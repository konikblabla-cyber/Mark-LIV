"""Read-only process handle summary on Windows."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_process_handles(parameters=None,**kwargs):
 p=parameters or {}; pid=max(0,int(p.get("pid",0)))
 if not pid:return "PID is required."
 cmd=f"Get-Process -Id {pid} -ErrorAction Stop | Select Id,ProcessName,HandleCount,Threads,Handles,WorkingSet64,CPU | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "Process not found or access denied.")[:6000]
TOOL={"name":"windows_process_handles","description":"Read-only process handle, thread, memory and CPU summary for a PID.","parameters":{"type":"OBJECT","properties":{"pid":{"type":"INTEGER"}},"required":["pid"]},"handler":windows_process_handles}
