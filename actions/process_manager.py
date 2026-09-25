"""Windows-only process management for Mark-LIV."""
import platform, subprocess
def process_manager(parameters=None, **kwargs):
    p=parameters or {}
    if platform.system()!="Windows": return "process_manager is available only on Windows."
    a=str(p.get("action","list")).lower().strip()
    if a=="list":
        r=subprocess.run(["powershell.exe","-NoProfile","-Command","Get-Process | Sort-Object CPU -Descending | Select-Object -First 100 Id,ProcessName,CPU,WorkingSet64 | Format-Table -AutoSize"],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
        return (r.stdout or r.stderr or "No process data.")[:12000]
    if a=="details":
        try:
            pid=int(p.get("pid",0))
        except (TypeError, ValueError):
            return "Valid PID required."
        if pid<=0: return "Valid PID required."
        r=subprocess.run(["powershell.exe","-NoProfile","-Command",f"Get-Process -Id {pid} | Select-Object * | Format-List"],capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
        return (r.stdout or r.stderr or "Process not found.")[:12000]
    if a=="stop":
        pid=int(p.get("pid",0))
        if pid<=0: return "Valid PID required."
        if pid in {0,4}: return "Protected system PID."
        r=subprocess.run(["taskkill.exe","/PID",str(pid),"/T"],capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
        return (r.stdout or r.stderr or f"Exit code: {r.returncode}")[:4000]
    return "Unknown process action."
TOOL={"name":"process_manager","description":"Windows process manager: list top processes, inspect a PID, or stop a process tree. Existing system-critical protections and normal Windows permissions remain in force.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING","description":"list | details | stop"},"pid":{"type":"INTEGER","description":"Process ID"}},"required":["action"]},"handler":process_manager}
