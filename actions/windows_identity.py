"""Windows identity and session information for Mark-LIV."""
import platform
import subprocess

def windows_identity(parameters=None, **kwargs):
    if platform.system() != "Windows":
        return "Windows-only action."
    p = parameters or {}
    a = str(p.get("action", "user")).lower().strip()
    cmds = {"user": ["whoami.exe"], "computer": ["powershell.exe","-NoProfile","-NonInteractive","-Command","$env:COMPUTERNAME"], "session": ["quser.exe"]}
    if a not in cmds:
        return "Use user, computer or session."
    try:
        r = subprocess.run(cmds[a], capture_output=True, text=True, timeout=15, creationflags=subprocess.CREATE_NO_WINDOW)
        return (r.stdout or r.stderr or "No identity data.")[:5000]
    except (OSError, subprocess.SubprocessError) as exc:
        return f"Could not read identity data: {exc}"

TOOL={"name":"windows_identity","description":"Windows-only identity/session diagnostics: current Windows user, computer name, or logged-on session information.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}},"required":["action"]},"handler":windows_identity}
