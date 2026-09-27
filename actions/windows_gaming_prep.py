"""Prepare Windows for gaming with reversible, low-risk settings."""
import platform
import subprocess
from core.permissions import permission_decision
from core import confirm

_TOKEN = object()

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=15, shell=False)

def windows_gaming_prep(parameters=None, _permission_token=None, **kwargs):
    if platform.system() != "Windows":
        return "Windows-only action."
    if _permission_token is not _TOKEN:
        p = parameters or {}
        decision = permission_decision("windows_gaming_prep", p)
        if decision == "deny":
            return "Permission denied."
        if decision == "confirm":
            return confirm.request("Prepare Windows for gaming", lambda _result: windows_gaming_prep(p, _permission_token=_TOKEN, **kwargs))
    try:
        parts = []
        r = run(["powercfg", "/setactive", "SCHEME_MIN"])
        if r.returncode == 0:
            parts.append("High-performance power plan activated.")
        else:
            parts.append("High-performance power plan could not be activated.")
        q = run(["reg", "add", r"HKCU\Software\Microsoft\GameBar", "/v", "AutoGameModeEnabled", "/t", "REG_DWORD", "/d", "1", "/f"])
        if q.returncode == 0:
            parts.append("Windows Game Mode enabled.")
        else:
            parts.append("Game Mode could not be changed.")
        return " ".join(parts)
    except (OSError, subprocess.SubprocessError) as exc:
        return f"Gaming preparation failed: {exc}"

TOOL={"name":"windows_gaming_prep","description":"Prepare Windows for gaming by activating High Performance power plan and enabling Game Mode; reversible settings only.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_gaming_prep}
