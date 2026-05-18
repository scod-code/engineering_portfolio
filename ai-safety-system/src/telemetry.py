import subprocess
import threading
import time
import json
import os
from pathlib import Path


def snapshotnetwork(label: str) -> list:
    """Capture current TCP/UDP connections using ss."""
    # ss is a Linux command-line tool that lists all active sockets: every open TCP and UDP connection on the machine at that moment.
    try:
        out = subprocess.run(["ss", "-tunp"], capture_output=True, text=True, timeout=5)
        lines = [l for l in out.stdout.splitlines() if l.strip() and "State" not in l]
        return [f"{label}:{l}" for l in lines]
    except Exception as e:
        return [f"ss_error:{e}"]


def snapshotopenfiles(pid: int) -> list:
    """Use lsof to list files opened by a process."""
    try:
        out = subprocess.run(["lsof", "-p", str(pid)], capture_output=True, text=True, timeout=5)
        return out.stdout.splitlines()
    except Exception:
        return []


def monitorprocess(pid: int, duration: int = 10) -> dict:
    """Poll CPU, memory, open files, and threads for a running process."""
    try:
        import psutil  #psutil is a Python library that can attach to any running process and read its resource usage in real time
        proc = psutil.Process(pid)
    except Exception as e:
        return {"error": str(e), "samples": []}
    samples = []
    stop = [False]

    def collect():
        proc.cpu_percent(None)
        while not stop[0]:
            try:
                samples.append({
                    "cpu":       proc.cpu_percent(interval=1),
                    "memmb":     proc.memory_info().rss / 1024 / 1024,
                    "openfiles": len(proc.open_files()),
                    "threads":   proc.num_threads()
                })
            except Exception:
                break

    t = threading.Thread(target=collect, daemon=True)
    t.start()
    time.sleep(duration)
    stop[0] = True
    t.join(timeout=3)
    return {
        "peakcpu":     max((s["cpu"]       for s in samples), default=0.0),
        "peakmemmb":   max((s["memmb"]     for s in samples), default=0.0),
        "peakfiles":   max((s["openfiles"] for s in samples), default=0),
        "peakthreads": max((s["threads"]   for s in samples), default=0),
        "samples":     samples
    }


def collecttelemetryfromsandboxresult(sandboxresult: dict, netbefore: list, netafter: list) -> dict:
    """Build dynamic features from sandbox output. Filters JupyterLab noise."""
    # Only flag genuinely new connections not owned by jupyter-lab itself
    new_raw = [l for l in netafter if l not in netbefore]
    new_external = [
        l for l in new_raw
        if "jupyter-lab" not in l
        and "127.0.0.1" not in l   # exclude loopback (JupyterLab IPC)
    ]
    return {
        "exitcode":        sandboxresult.get("exit_code", sandboxresult.get("exitcode", 0)),
        "timedout":        int(sandboxresult.get("timed_out", sandboxresult.get("timedout", False))),
        "networkattempts": len(new_external),
        "procspawns":      sandboxresult.get("stdout", "").count("Traceback"),
        "peakcpu":         0.0,
        "peakmemmb":       0.0,
        "newconnections":  new_external,        # list — skipped by compute_risk
        "stderrnonempty":  int(bool(sandboxresult.get("stderr", "").strip()))
    }


def savetelemetrylog(telemetry: dict, scriptname: str, logdir: str = "logs") -> str:
    """Write telemetry dict to a JSON log file. Returns the saved file path."""
    os.makedirs(logdir, exist_ok=True)
    safename = scriptname.replace("/", "_").replace("\\", "_")
    logpath = os.path.join(logdir, f"{safename}_telemetry.json")
    Path(logpath).write_text(json.dumps(telemetry, indent=2))
    return logpath
