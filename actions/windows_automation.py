"""Windows-only high-level automation helpers for Mark-LIV."""
import platform, subprocess, os, json
from pathlib import Path

def windows_automation(parameters=None, **kwargs):
 if platform.system()!="Windows": return "Windows-only action."
    p=parameters or {}; a=str(p.get("action","")).lower().strip()
    flags=subprocess.CREATE_NO_WINDOW
    if a=="run":
        command=str(p.get("command","")).strip()
        if not command: return "Command is required."
        if len(command)>4000: return "Command too long."
        r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",command],capture_output=True,text=True,timeout=60,creationflags=flags)
        out=(r.stdout or "").strip(); err=(r.stderr or "").strip()
        return (out or err or f"Exit code: {r.returncode}")[:12000]
    if a=="open":
        target=str(p.get("target") or p.get("path") or p.get("url") or p.get("name") or "").strip().strip('"')
        if not target: return "Target is required."
        if len(target)>1000: return "Target is too long."
        # Windows Shell resolves URLs, registered applications, files and folders.
        subprocess.Popen(["powershell.exe","-NoProfile","-NonInteractive","-Command","Start-Process -FilePath $args[0]"],args=[target],creationflags=flags)
        return f"Opened: {target}"
    if a=="run_program":
        exe=str(p.get("program") or p.get("path") or "").strip().strip('"')
        args=p.get("args") or []
        if not exe:return "Program path is required."
        if not isinstance(args,list):args=[str(args)]
        if len(args)>30:return "Too many program arguments."
        try:
            proc=subprocess.Popen([exe,*[str(x) for x in args]],cwd=str(p.get("cwd") or "") or None,creationflags=flags)
            return f"Started program: {exe} (PID {proc.pid})"
        except Exception as e:return f"Program start failed: {e}"
    if a=="run_and_capture":
        command=str(p.get("command","")).strip()
        if not command:return "Command is required."
        timeout=max(1,min(int(p.get("timeout",60)),180))
        rr=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",command],capture_output=True,text=True,timeout=timeout,creationflags=flags)
        return json.dumps({"exit_code":rr.returncode,"stdout":(rr.stdout or "")[:12000],"stderr":(rr.stderr or "")[:12000]},ensure_ascii=False)
    if a=="open_url":
        url=str(p.get("url","")).strip()
        if not (url.startswith("https://") or url.startswith("http://")): return "Only http/https URLs are allowed."
        os.startfile(url); return f"Opened URL: {url}"
    if a=="open_path":
        path=Path(str(p.get("path","")).strip().strip('"')).expanduser()
        if not path.exists(): return f"Path not found: {path}"
        os.startfile(str(path)); return f"Opened: {path}"
    return "Unknown Windows automation action."

TOOL={"name":"windows_automation","description":"Windows-only automation: universal open for Windows Shell targets (apps, files, folders and URLs), plus PowerShell, URL and local-path opening. Uses normal Windows permissions/UAC; no security bypass.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING","description":"open | run | run_program | run_and_capture | open_url | open_path"},"command":{"type":"STRING","description":"PowerShell command"},"url":{"type":"STRING","description":"http/https URL"},"path":{"type":"STRING","description":"Existing Windows path"},"target":{"type":"STRING","description":"Universal Windows Shell target: app, file, folder or URL"},"name":{"type":"STRING","description":"Application or target name"}},"required":["action"]},"handler":windows_automation}
