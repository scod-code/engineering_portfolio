from typing import Dict, Any

# =============================================================================
# Requirement 9 — Multi-Agent Monitoring and Orchestrator
# Source: Lab 7 — Agentic Monitoring (COMP40771)
#
# DESIGN PRINCIPLE: Each class below implements the sense-reason-act loop
# from Lab 7. "Agentic monitoring extends monitoring from passive reporting
# into conditional decision-making."
#
# WHY FOUR SEPARATE AGENTS instead of one monolithic monitor?
#   - Each agent maps directly to one threat category from the Req 1 threat
#     model (network exfiltration, subprocess abuse, resource abuse,
#     filesystem/credential access).
#   - A single monitoring function would couple all threat logic together.
#     If one channel's weight needed recalibrating, you would risk breaking
#     the others. Here, each agent can be updated independently.
#   - Two independent channels agreeing (e.g., fs AND net both scoring high)
#     is stronger evidence than one channel alone — reduces false positives.
#
# RELATIONSHIP TO OTHER REQUIREMENTS:
#   - Input: the telemetry dict produced by collect_telemetry_from_sandbox_result()
#     in src/telemetry.py (Req 5).
#   - Output: a decision string that can trigger the MQTT alert in
#     src/mqtt_publish.py (Req 14) or be logged to MongoDB via src/mongostore.py
#     (Req 12).
#   - Distinct from compute_risk() in src/risk.py (Req 3): compute_risk()
#     produces a static weighted score for a report. The Orchestrator produces
#     an *actionable decision* (terminate / restrict / pause / continue).
# =============================================================================

class FilesystemAgent:
    def sense(self, telemetry: dict) -> Any:
        return telemetry.get("newconnections", []) or telemetry.get("fswrites", 0)
    def assess(self, data) -> dict:
        count = data if isinstance(data, int) else len(data)
        return {"channel": "fs", "score": round(count * 1.5, 2)}

class NetworkAgent:
    def sense(self, telemetry: dict) -> Any:
        return telemetry.get("networkattempts", 0)
    def assess(self, data) -> dict:
        return {"channel": "net", "score": round(float(data) * 4.0, 2)}

class ProcessAgent:
    def sense(self, telemetry: dict) -> Any:
        return telemetry.get("procspawns", 0)
    def assess(self, data) -> dict:
        return {"channel": "proc", "score": round(float(data) * 2.0, 2)}

class ResourceAgent:
"""
    Req 1 threat covered: resource abuse (CPU exhaustion, near-fork-bombs,
    infinite loops consuming CPU share).

    Monitors 'peak_cpu' — the peak CPU percentage recorded by the threaded
    psutil sampler in monitor_process() (Req 5).

    THRESHOLD DESIGN: only CPU usage ABOVE 80% scores anything.
    - max(0, data - 80): negative values are clamped to zero, so normal
      CPU-intensive but legitimate scripts (e.g., sorting 10k items) do not
      accumulate score just for working hard.
    - Coefficient 0.1: a script pegged at 100% CPU scores only
      (100 - 80) × 0.1 = 2.0 — deliberately a supporting signal, not a
      dominant one. Resource abuse rarely appears in isolation; it is most
      meaningful when paired with network or process signals.
    """
    def sense(self, telemetry: dict) -> Any:
        return telemetry.get("peakcpu", 0.0)
    def assess(self, data) -> dict:
        return {"channel": "resource", "score": round(max(0, float(data) - 80) * 0.1, 2)}

class Orchestrator:
    def __init__(self):
        self.agents = [FilesystemAgent(), NetworkAgent(), ProcessAgent(), ResourceAgent()]

"""
    Implements the ACT step of the sense-reason-act loop (Lab 7).

    The Orchestrator does not monitor any channel directly. Its sole
    responsibility is to fuse the independent assessments from all four
    specialist agents into a single actionable decision.

    WHY A FOUR-TIER ESCALATION LADDER instead of a binary safe/dangerous?
    - Binary decisions are brittle: one noisy signal flips the verdict.
    - Graduated responses are proportional to the weight of evidence:
        CONTINUE  (< 4):  all channels quiet; no action needed.
        PAUSE     (4–8):  mild signal; hold execution and observe further.
        RESTRICT  (8–15): clear multi-channel signal; quarantine and alert.
        TERMINATE (≥15):  definitive threat; kill process and escalate.
    - This mirrors Lab 7's four-tier response architecture directly.

    RELATIONSHIP TO compute_risk() (Req 3):
    - compute_risk() produces a float score + label for an audit report.
    - Orchestrator.fuse() produces a decision string for automated response.
    - In a deployed system, TERMINATE would trigger the MQTT alert (Req 14)
      and kill the Docker container (Req 4).
    """

    def fuse(self, telemetry: dict) -> dict:
        reports = [a.assess(a.sense(telemetry)) for a in self.agents]
        total   = sum(r["score"] for r in reports)
        if total >= 15:   decision = "terminate"
        elif total >= 8:  decision = "restrict"
        elif total >= 4:  decision = "pause"
        else:             decision = "continue"
        return {"total": round(total, 2), "decision": decision, "reports": reports}