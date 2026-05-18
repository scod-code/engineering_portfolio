import ast
from pathlib import Path

RISKY_IMPORTS = {
    "subprocess", "os", "socket", "requests", "urllib",
    "ctypes", "pickle", "importlib", "base64", "marshal",
    "http", "ftplib", "smtplib", "telnetlib", "paramiko"
}

RISKY_CALLS = {"eval", "exec", "compile", "getattr", "setattr", "__import__"}

SUBPROCESS_CALLS = {"system", "popen", "run", "Popen", "check_output", "call"}

NETWORK_CALLS = {"connect", "get", "post", "urlopen", "urlretrieve", "send", "sendto"}

FS_WRITE_CALLS = {"open", "write", "writelines", "unlink", "remove", "rmtree", "rename"}

OBFUSCATION_CALLS = {"b64decode", "b64encode", "decompress", "loads", "fromhex", "unhexlify"}


def extract_features(source: str) -> dict:
    """Parse source code and return a feature dict without executing it."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {"parse_error": 1, "risky_imports": 0, "eval_exec": 0,
                "subprocess_calls": 0, "network_calls": 0, "fs_writes": 0, "obfuscation": 0}

    features = {k: 0 for k in [
        "parse_error", "risky_imports", "eval_exec",
        "subprocess_calls", "network_calls", "fs_writes", "obfuscation"
    ]}

    for node in ast.walk(tree):
        # Risky top-level imports
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in RISKY_IMPORTS:
                    features["risky_imports"] += 1

        # Risky from-imports
        if isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in RISKY_IMPORTS:
                features["risky_imports"] += 1

        # Function calls
        if isinstance(node, ast.Call):
            func_name = ""
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                func_name = node.func.attr

            if func_name in RISKY_CALLS:
                features["eval_exec"] += 1
            if func_name in SUBPROCESS_CALLS:
                features["subprocess_calls"] += 1
            if func_name in NETWORK_CALLS:
                features["network_calls"] += 1
            if func_name in FS_WRITE_CALLS:
                features["fs_writes"] += 1
            if func_name in OBFUSCATION_CALLS:
                features["obfuscation"] += 1

    return features


def analyse_file(path: str) -> dict:
    """Read a file from disk and extract its features."""
    source = Path(path).read_text(encoding="utf-8", errors="replace")
    feats = extract_features(source)
    feats["file"] = str(path)
    return feats


if __name__ == "__main__":
    import sys, json
    if len(sys.argv) > 1:
        result = analyse_file(sys.argv[1])
        print(json.dumps(result, indent=2))
