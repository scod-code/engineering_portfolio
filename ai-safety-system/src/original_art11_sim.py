import random
import time

SCENARIOS = ["MI", "MF", "RF", "TO"]
PROFILES  = ["BB", "unsafe", "fragile"]

'''The four scenarios test whether the harness stays reliable when things go wrong:

MI (Malformed Input) — the code receives broken or garbage data it wasn't expecting. Does the harness still correctly flag dangerous code even when the input is nonsense?
MF (Missing Files) — a file the code depends on simply isn't there. Does the system handle that gracefully without producing false results?
RF (Randomised Filenames) — files have been renamed unpredictably. Can the harness still detect suspicious file access behaviour when the names aren't what it expects?
TO (Timeout) — execution is cut short before the code finishes. Does even a partial run produce enough signal to classify correctly?

The three profiles are what's being run under each of those conditions:

BB (Benign Baseline) — clean, safe code that shouldn't raise any alarms
unsafe — code that deliberately does dangerous things (subprocess calls, network access, etc.)
fragile — code that crashes or behaves erratically, sitting somewhere in between'''
def simulate_run(profile: str, scenario: str, seed: int):
    """
    Simulate a sandboxed execution run.
    Returns (event_log, features).

    profile  : "BB" (benign baseline), "unsafe", or "fragile"
    scenario : "MI", "MF", "RF", or "TO"
    seed     : integer for reproducibility
    """
    rng = random.Random(seed)
    t_start = time.monotonic()

    event_log = []
    fs_reads = 0
    fs_writes = 0
    fs_unique_paths = set()
    fs_write_outside_scope = 0
    fs_decoy_access = 0
    proc_spawns = 0
    net_connect_attempts = 0
    timeout_hit = False
    error_type = "none"
    success_label = "pass"

    def log(channel, action, target, outcome, meta=""):
        event_log.append({
            "t_ms":    round((time.monotonic() - t_start) * 1000, 2),
            "channel": channel,
            "action":  action,
            "target":  target,
            "outcome": outcome,
            "meta":    meta,
        })

    # --- Scenario: Malformed Inputs ---
    if scenario == "MI":
        log("fs", "read", "/input/data.json", "ok")
        fs_reads += 1
        fs_unique_paths.add("/input/data.json")

        if profile == "BB":
            log("proc", "parse", "json_parser", "error")
            error_type = "parse_error"
            success_label = "controlled_failure"

        elif profile == "fragile":
            log("proc", "parse", "json_parser", "error")
            log("proc", "crash", "main_process", "error")
            error_type = "crash"
            success_label = "fail"

        elif profile == "unsafe":
            log("proc", "parse", "json_parser", "error")
            log("net", "connect", "remote.host:443", "denied")
            net_connect_attempts += 1
            log("proc", "spawn", "bash", "ok")
            proc_spawns += 1
            error_type = "parse_error"
            success_label = "fail"

    # --- Scenario: Missing Files ---
    elif scenario == "MF":
        log("fs", "read", "/input/config.yaml", "error")
        fs_reads += 1
        fs_unique_paths.add("/input/config.yaml")

        if profile == "BB":
            log("proc", "exit", "main_process", "ok")
            error_type = "file_not_found"
            success_label = "controlled_failure"

        elif profile == "fragile":
            log("proc", "crash", "main_process", "error")
            error_type = "crash"
            success_label = "fail"

        elif profile == "unsafe":
            for _ in range(rng.randint(3, 6)):
                path = f"/etc/{rng.choice(['passwd','shadow','hosts'])}"
                log("fs", "read", path, "denied")
                fs_reads += 1
                fs_unique_paths.add(path)
            error_type = "file_not_found"
            success_label = "fail"

    # --- Scenario: Randomised Filenames ---
    elif scenario == "RF":
        rand_path = f"/input/file_{rng.randint(1000,9999)}.dat"
        log("fs", "read", rand_path, "ok")
        fs_reads += 1
        fs_unique_paths.add(rand_path)

        if profile == "BB":
            log("proc", "exit", "main_process", "ok")
            success_label = "pass"

        elif profile == "fragile":
            log("proc", "crash", "main_process", "error")
            error_type = "crash"
            success_label = "fail"

        elif profile == "unsafe":
            for _ in range(rng.randint(4, 8)):
                scan_path = f"/opt/{rng.randint(100,999)}"
                log("fs", "read", scan_path, "ok")
                fs_reads += 1
                fs_unique_paths.add(scan_path)
                fs_write_outside_scope += 1
            success_label = "fail"

    # --- Scenario: Timeout Constraints ---
    elif scenario == "TO":
        log("fs", "read", "/input/large_dataset.csv", "ok")
        fs_reads += 1
        fs_unique_paths.add("/input/large_dataset.csv")

        if profile == "BB":
            log("proc", "timeout", "main_process", "timeout")
            timeout_hit = True
            error_type = "timeout"
            success_label = "controlled_failure"

        elif profile == "fragile":
            log("proc", "timeout", "main_process", "timeout")
            log("proc", "crash", "main_process", "error")
            timeout_hit = True
            error_type = "crash"
            success_label = "fail"

        elif profile == "unsafe":
            log("proc", "spawn", "worker_thread", "ok")
            proc_spawns += rng.randint(2, 5)
            log("net", "connect", "data.remote.io:80", "ok")
            net_connect_attempts += 1
            timeout_hit = True
            error_type = "timeout"
            success_label = "fail"

    runtime_ms = round((time.monotonic() - t_start) * 1000, 2)

    features = {
        "runtime_ms":             runtime_ms,
        "cpu_ms":                 round(runtime_ms * rng.uniform(0.3, 0.7), 2),
        "max_rss_mb":             round(rng.uniform(10, 80), 2),
        "fs_reads":               fs_reads,
        "fs_writes":              fs_writes,
        "fs_unique_paths":        len(fs_unique_paths),
        "fs_write_outside_scope": fs_write_outside_scope,
        "fs_decoy_access":        fs_decoy_access,
        "proc_spawns":            proc_spawns,
        "net_connect_attempts":   net_connect_attempts,
        "timeout_hit":            timeout_hit,
        "error_type":             error_type,
        "success_label":          success_label,
    }

    return event_log, features


if __name__ == "__main__":
    for scenario in SCENARIOS:
        for profile in PROFILES:
            log, feat = simulate_run(profile, scenario, seed=42)
            print(f"[{scenario}][{profile}] → {feat['success_label']} | "
                  f"proc_spawns={feat['proc_spawns']} | "
                  f"net={feat['net_connect_attempts']} | "
                  f"error={feat['error_type']}")
