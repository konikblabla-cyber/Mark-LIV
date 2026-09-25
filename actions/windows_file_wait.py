"""Wait for a Windows file or folder to appear."""
import os, platform, time

def windows_file_wait(parameters=None, **kwargs):
    if platform.system() != "Windows":
        return "windows_file_wait is Windows-only."
    p = parameters or {}
    path = str(p.get("path") or "").strip()
    try:
        timeout = max(1, min(int(p.get("timeout", 30)), 120))
    except (TypeError, ValueError):
        return "Invalid timeout."
    if not path:
        return "Missing path."
    expanded = os.path.expandvars(path)
    end = time.time() + timeout
    while time.time() < end:
        if os.path.exists(expanded):
            return f"Path appeared: {expanded}"
        time.sleep(0.5)
    return f"Path did not appear within {timeout}s: {path}"

TOOL={"name":"windows_file_wait","description":"Wait for a Windows file or folder to appear, useful in multi-step tasks.","parameters":{"type":"OBJECT","properties":{"path":{"type":"STRING"},"timeout":{"type":"INTEGER"}},"required":["path"]},"handler=windows_file_wait}
