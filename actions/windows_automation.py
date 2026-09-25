"""Windows-only high-level automation helpers for Mark-LIV."""
import platform, subprocess, os
from pathlib import Path
if platform.system() != "Windows":
    raise RuntimeError("Mark-LIV Windows automation is Windows-only.")

def windows_automation(parameters=None, **kwargs):
    p=parameters or {}; a=str(p.get("action","")).lower().strip()
    flags=subprocess.CREATE_NO_WINDOW
    if a=="run":
        command=str(p.get("command","")).strip()
        if not command: return "Command is required."
        if len(command)>4000: return "Command too long."
        r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",command],capture_output=True,text=True,timeout=60,creationflags=flags)
        out=(r.stdout or "").strip(); err=(r.stderr or "").strip()
        return (out or err or f"Exit code: {r.returncode}")[:12000]
    if a=="open_url":
        url=str(p.get("url","")).strip()
        if not (url.startswith("https://") or url.startswith("http://")): return "Only http/https URLs are allowed."
        os.startfile(url); return f"Opened URL: {url}"
    if a=="open_path":
        path=Path(str(p.get("path","")).strip().strip('"')).expanduser()
        if not path.exists(): return f"Path not found: {path}"
        os.startfile(str(path)); return f"Opened: {path}"
    return "Unknown Windows automation action."

TOOL={"name":"windows_automation","description":"Windows-only automation: run a PowerShell command, open a trusted http/https URL, or open an existing local path. Use normal Windows permissions/UAC; no security bypass.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING","description":"run | open_url | open_path"},"command":{"type":"STRING","description":"PowerShell command"},"url":{"type":"STRING","description":"http/https URL"},"path":{"type":"STRING","description":"Existing Windows path"}},"required":["action"]},"handler":windows_automation}
