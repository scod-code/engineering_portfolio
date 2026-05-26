import json


def load_config(config_path: str = "config/default.json") -> dict:
    with open(config_path, "r") as f:
        return json.load(f)


def save_config(path: str, cfg: dict) -> None:
    with open(path, "w") as f:
        json.dump(cfg, f, indent=2)


def compute_risk(static_features: dict, dynamic_features: dict, weights: dict) -> tuple:
    breakdown = {}
    for key, val in static_features.items():
        if not isinstance(val, (int, float)):
            continue
        w = weights.get(key, 1.0)
        contribution = round(w * float(val), 2)
        if contribution > 0:
            breakdown[f"static_{key}"] = contribution
    for key, val in dynamic_features.items(): #same principle, but keys are from telemetry (e.g., network_attempts, proc_spawns, peak_cpu)
        if not isinstance(val, (int, float)):
            continue
        w = weights.get(key, 1.0)
        contribution = round(w * float(val), 2)
        if contribution > 0:
            breakdown[f"dynamic_{key}"] = contribution
    score = round(sum(breakdown.values()), 2)
    return score, breakdown


def classify_risk(score: float) -> str:
    if score >= 15:
        return "CRITICAL"
    elif score >= 8:
        return "HIGH"
    elif score >= 4:
        return "MEDIUM"
    elif score > 0:
        return "LOW"
    return "CLEAN"
