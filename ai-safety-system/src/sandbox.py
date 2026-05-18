import subprocess
import sys
import os
import resource
import shutil
from pathlib import Path


def _apply_limits(memory_bytes: int, cpu_seconds: int, max_procs: int):
    """Called as preexec_fn inside the child process to set OS resource limits."""
    # Memory (virtual address space)
    resource.setrlimit(resource.RLIMIT_AS,   (memory_bytes, memory_bytes))
    # CPU time
    resource.setrlimit(resource.RLIMIT_CPU,  (cpu_seconds,  cpu_seconds))
    # Number of child processes (blocks fork bombs)
    resource.setrlimit(resource.RLIMIT_NPROC,(max_procs,    max_procs))


def run_in_sandbox(script_path: str, cfg: dict) -> dict:
    """
    Execute a script in a resource-limited subprocess.
    Uses OS-level RLIMIT enforcement. Works correctly from inside a container.
    """
    sb        = cfg["sandbox"]
    workspace = os.path.abspath("workspace")
    os.makedirs(workspace, exist_ok=True)

    script_name = os.path.basename(script_path)
    dest        = os.path.join(workspace, script_name)

    if os.path.abspath(script_path) != os.path.abspath(dest):
        shutil.copy2(script_path, dest)

    mem_bytes   = _parse_memory(sb["memory_limit"])
    cpu_seconds = max(1, int(sb.get("cpu_quota", 0.5) * sb["timeout_seconds"]))
    max_procs   = sb.get("max_procs", 32)
    timeout     = sb["timeout_seconds"]

    try:
        result = subprocess.run(
            [sys.executable, dest],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=workspace,
            preexec_fn=lambda: _apply_limits(mem_bytes, cpu_seconds, max_procs)
        )
        return {
            "exit_code": result.returncode,
            "stdout":    result.stdout[:2000],
            "stderr":    result.stderr[:2000],
            "timed_out": False
        }
    except subprocess.TimeoutExpired:
        return {
            "exit_code": -1,
            "stdout":    "",
            "stderr":    f"Timed out after {timeout}s",
            "timed_out": True
        }
    except Exception as e:
        return {
            "exit_code": -3,
            "stdout":    "",
            "stderr":    str(e),
            "timed_out": False
        }


def _parse_memory(limit_str: str) -> int:
    """Convert strings like '256m', '512m', '1g' to bytes."""
    s = str(limit_str).strip().lower()
    if s.endswith("g"):
        return int(float(s[:-1]) * 1024 ** 3)
    if s.endswith("m"):
        return int(float(s[:-1]) * 1024 ** 2)
    if s.endswith("k"):
        return int(float(s[:-1]) * 1024)
    return int(s)


def sandbox_command_preview(cfg: dict, script_name: str = "<script.py>") -> str:
    """Human-readable description of the sandbox constraints being applied."""
    sb        = cfg["sandbox"]
    workspace = os.path.abspath("workspace")
    mem_bytes = _parse_memory(sb["memory_limit"])
    cpu_s     = max(1, int(sb.get("cpu_quota", 0.5) * sb["timeout_seconds"]))
    lines = [
        "# Sandbox: subprocess inside existing container with OS resource limits",
        f"# Memory limit  : {sb['memory_limit']} (RLIMIT_AS = {mem_bytes // 1024 // 1024} MB)",
        f"# CPU limit     : {cpu_s}s (RLIMIT_CPU)",
        f"# Wall timeout  : {sb['timeout_seconds']}s",
        f"# Max processes : {sb.get('max_procs', 32)} (RLIMIT_NPROC)",
        f"# Working dir   : {workspace}",
        f"# Script        : {workspace}/{script_name}",
        f"# Interpreter   : {sys.executable}",
    ]
    return "\n".join(lines)

def plant_canaries(workspace_dir: str) -> list:
    import os
    canaries = [
        ("decoy_token.txt", "CANARY_API_KEY=sk-fake-canary-abc123"),
        (".env",            "DB_PASSWORD=canary_db_password_xyz"),
    ]
    for fname, content in canaries:
        with open(os.path.join(workspace_dir, fname), "w") as f:
            f.write(content)
    return [fname for fname, _ in canaries]


def check_canary_access(telemetry: dict, canaries: list) -> bool:
    accessed = telemetry.get("newconnections", []) + [str(telemetry)]
    return any(c in str(accessed) for c in canaries)
