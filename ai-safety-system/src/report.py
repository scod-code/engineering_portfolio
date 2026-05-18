from datetime import datetime
import os


def _classify(score: float) -> str:
    if score >= 15:
        return "CRITICAL"
    elif score >= 8:
        return "HIGH"
    elif score >= 4:
        return "MEDIUM"
    elif score > 0:
        return "LOW"
    return "CLEAN"

# Uses hard-coded conditional logic - if a signal is detected,
# a specific mitigation is appended
def generate_report(
    score: float,
    breakdown: dict,
    telemetry: dict,
    static_features: dict = None,
    script_name: str = "<unknown>",
    policy: str = "continue"
) -> str:
    static_features = static_features or {}

    lines = []
    lines.append("## Risk Report")
    lines.append(f"**Script:** {script_name}")
    lines.append(f"**Evaluated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Overall Score:** {score}")
    lines.append(f"**Risk Label:** {_classify(score)}")
    lines.append("")
    lines.append("### Score Breakdown")

    shown = False
    for k, v in sorted(breakdown.items(), key=lambda x: -x[1]):
        if isinstance(v, (int, float)) and v > 0:
            lines.append(f"- `{k}`: {v}")
            shown = True
    if not shown:
        lines.append("- No positive risk signals detected.")

    lines.append("")
    lines.append("### Static Signals")
    static_shown = False
    for k, v in static_features.items():
        if isinstance(v, (int, float)) and v > 0:
            lines.append(f"- `{k}`: {v}")
            static_shown = True
    if not static_shown:
        lines.append("- No static signals detected.")

    lines.append("")
    lines.append("### Dynamic Signals")
    dynamic_keys = [
        "exitcode", "timedout", "networkattempts",
        "procspawns", "peakcpu", "peakmemmb", "stderrnonempty"
    ]
    dynamic_shown = False
    for k in dynamic_keys:
        v = telemetry.get(k, 0)
        if isinstance(v, (int, float)) and v != 0:
            lines.append(f"- `{k}`: {v}")
            dynamic_shown = True
    if not dynamic_shown:
        lines.append("- No dynamic signals detected.")

    lines.append("")
    lines.append("### Recommended Mitigations")
    mitigations = []

    if breakdown.get("static_eval_exec", 0) > 0:
        mitigations.append("Remove use of `eval`/`exec`; use safe parsing alternatives.")
    if breakdown.get("static_subprocess_calls", 0) > 0:
        mitigations.append("Avoid `subprocess` unless absolutely necessary; never use `shell=True`.")
    if breakdown.get("static_risky_imports", 0) > 0:
        mitigations.append("Review imported modules and restrict to task-required libraries only.")
    if telemetry.get("networkattempts", 0) > 0:
        mitigations.append("Enforce `--network none` and investigate outbound connection attempts.")
    if telemetry.get("timedout", 0):
        mitigations.append("Investigate timeout behaviour for possible infinite loops or resource abuse.")
    if telemetry.get("stderrnonempty", 0):
        mitigations.append("Inspect stderr output for crashes, parsing failures, or blocked operations.")

    if not mitigations:
        mitigations.append("No specific mitigations required.")

    for m in mitigations:
        lines.append(f"- {m}")

    lines.append("")
    lines.append(f"### Decision: `{policy.upper()}`")
    return "\n".join(lines)


def save_report(report_str: str, script_name: str, outdir: str = "outputs") -> str:
    os.makedirs(outdir, exist_ok=True)
    safe = script_name.replace("/", "_").replace("\\", "_")
    path = os.path.join(outdir, f"{safe}_report.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(report_str)
    return path


def print_report(report: dict) -> None:
    print(report["explanation"])

def generate_behavioral_report(
    telemetry: dict,
    score: float,
    breakdown: dict,
    label: str,
    script_name: str = "<unknown>"
) -> str:
    """Lab 10-style behavioral explanation — richer than basic report."""
    from datetime import datetime
    lines = []
    lines.append(f"Behavioral Risk Classification: {label}  (confidence score: {score:.2f})")
    lines.append(f"Script: {script_name}  |  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("Observed Indicators:")

    if telemetry.get("networkattempts", 0) > 0:
        lines.append(f"  - Outbound network connections detected: {telemetry['networkattempts']}")
    if telemetry.get("timedout", 0):
        lines.append("  - Script exceeded sandbox timeout — potential fork bomb or infinite loop")
    if telemetry.get("procspawns", 0) > 0:
        lines.append(f"  - Subprocess spawns detected: {telemetry['procspawns']}")
    if telemetry.get("stderrnonempty", 0):
        lines.append("  - Non-empty stderr — runtime errors or crash output present")

    lines.append("")
    lines.append("Score Breakdown:")
    for k, v in sorted(breakdown.items(), key=lambda x: -x[1]):
        lines.append(f"  {k:<40} {v:>6.2f}")

    lines.append("")
    lines.append("Primary Risk Contributors:")
    for k, v in sorted(breakdown.items(), key=lambda x: -x[1])[:3]:
        if v > 0:
            lines.append(f"  - {k}: {v}")

    lines.append("")
    lines.append("Recommended Action:")
    if score >= 15 or label == "CRITICAL":
        lines.append("  TERMINATE — Do not execute. Forensic capture advised.")
    elif score >= 8 or label == "HIGH":
        lines.append("  RESTRICT — Manual review required before any execution.")
    elif score >= 4 or label == "MEDIUM":
        lines.append("  PAUSE — Flag for review. Proceed only under supervision.")
    else:
        lines.append("  CONTINUE — Consistent with benign code. Monitor passively.")

    return "\n".join(lines)
