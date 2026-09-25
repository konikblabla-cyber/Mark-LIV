"""Read-only Windows process start-time inspector."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_process_start_time(parameters=None,**kwargs):
 p=parameters or {}; pid=max(1,int(p.get("pid",0)))
 cmd=f"Get-Process -Id {pid} -ErrorAction Stop | Select Id,ProcessName,StartTime,Responding,Path | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "Process not found or access denied.")[:7000]
TOOL={"name":"windows_process_start_time","description":"Read-only Windows process start time and responsiveness inspection by PID.","parameters":{"type":"OBJECT","properties":{"pid":{"type":"INTEGER"}},"required":["pid"]},"handler":windows_process_start_time}
