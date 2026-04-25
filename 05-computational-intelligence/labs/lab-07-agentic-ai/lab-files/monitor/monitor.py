import os, time, json, re, requests

API_BASE = os.getenv("API_BASE", "http://localhost:8000")
OLLAMA_BASE = os.getenv("OLLAMA_BASE", "http://localhost:11434")
MODEL_LIGHT = os.getenv("MODEL_LIGHT", "llama3.2:1b")
MODEL_HEAVY = os.getenv("MODEL_HEAVY", "phi3:mini")
ESCALATION_WEBHOOK = os.getenv("ESCALATION_WEBHOOK", "").strip()

POLL_SECONDS = 10

def fetch_metrics_text() -> str:
    r = requests.get(f"{API_BASE}/metrics", timeout=5)
    r.raise_for_status()
    return r.text

def parse_metric(metrics_text: str, name: str) -> float:
    total = 0.0
    for line in metrics_text.splitlines():
        if line.startswith("#"):
            continue
        if line.startswith(name + "{") or line.startswith(name + " "):
            parts = line.split()
            if len(parts) >= 2:
                try:
                    total += float(parts[-1])
                except ValueError:
                    pass
    return total

def ollama_generate(model: str, prompt: str) -> str:
    payload = {"model": model, "prompt": prompt, "stream": False}
    r = requests.post(f"{OLLAMA_BASE}/api/generate", json=payload, timeout=30)
    r.raise_for_status()
    return r.json().get("response", "").strip()

def triage_with_llm(model: str, context: dict) -> dict:
    prompt = (
        "You are an SRE triage assistant.\n"
        "Given the monitoring context, output STRICT JSON with keys:\n"
        "\"severity\" (low|medium|high|critical), confidence (0-1), summary, recommended_action.\n"
        "No extra text.\n\n"
        f"Context:\n{json.dumps(context, indent=2)}\n"
    )
    raw = ollama_generate(model, prompt)
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if not m:
        return {"severity": "medium", "confidence": 0.3,
                "summary": "Model output not parseable.",
                "recommended_action": "Inspect metrics manually."}
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return {"severity": "medium", "confidence": 0.3,
                "summary": "JSON decode failed.",
                "recommended_action": "Inspect metrics manually."}

def should_escalate(assessment: dict, error_rate_delta: float, latency_hint: bool) -> str:
    sev = assessment.get("severity", "medium")
    conf = float(assessment.get("confidence", 0.0))
    # Deterministic guardrails — always override model
    if error_rate_delta >= 5:
        return "human"
    if latency_hint and sev in ("high", "critical"):
        return "human"
    # Confidence-based escalation
    if sev in ("high", "critical") and conf < 0.7:
        return "heavy"
    if sev == "medium" and conf < 0.5:
        return "heavy"
    return "none"

def notify_human(message: str):
    print(f"[ESCALATE:HUMAN] {message}")
    if ESCALATION_WEBHOOK:
        try:
            requests.post(ESCALATION_WEBHOOK, json={"text": message}, timeout=5)
        except Exception:
            print("[WARN] Webhook failed")

def main():
    print("[monitor] starting")
    prev_errors = None
    prev_reqs = None

    while True:
        try:
            metrics = fetch_metrics_text()
            errors_total = parse_metric(metrics, "errors_total")
            reqs_total = parse_metric(metrics, "requests_total")

            if prev_errors is None:
                prev_errors, prev_reqs = errors_total, reqs_total
                time.sleep(POLL_SECONDS)
                continue

            errors_delta = errors_total - prev_errors
            reqs_delta = max(reqs_total - prev_reqs, 0.0)
            latency_hint = False  # Extended in Task C

            context = {
                "window_seconds": POLL_SECONDS,
                "requests_delta": reqs_delta,
                "errors_delta": errors_delta,
                "api_base": API_BASE
            }

            assessment_light = triage_with_llm(MODEL_LIGHT, context)
            decision = should_escalate(assessment_light, errors_delta, latency_hint)
            print(f"[monitor] light_assessment={assessment_light} decision={decision}")

            if decision == "heavy":
                assessment_heavy = triage_with_llm(MODEL_HEAVY, context)
                print(f"[monitor] heavy_assessment={assessment_heavy}")
                if assessment_heavy.get("severity") in ("high", "critical"):
                    notify_human(json.dumps(assessment_heavy))
            elif decision == "human":
                notify_human(json.dumps({"light_assessment": assessment_light, "context": context}))

            prev_errors, prev_reqs = errors_total, reqs_total

        except Exception as e:
            print(f"[monitor] error={type(e).__name__} msg={e}")

        time.sleep(POLL_SECONDS)

if __name__ == "__main__":
    main()
