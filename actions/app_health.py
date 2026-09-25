"""Windows application responsiveness checks for Mark-LIV."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def app_health(parameters=None,**kwargs):
 p=parameters or {}; name=str(p.get("process","")).strip()
 if not name:return "Process executable name is required."
 base=name.rsplit(".",1)[0].replace("'","''")
 cmd=f"Get-Process -Name '{base}' -ErrorAction SilentlyContinue | Select Id,ProcessName,Responding,CPU,WorkingSet64,StartTime | Format-Table -AutoSize"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or f"{name} is not running.")[:8000]
TOOL={"name":"app_health","description":"Windows-only app health check: reports PID, responsiveness, CPU, memory and start time for an executable.","parameters":{"type":"OBJECT","properties":{"process":{"type":"STRING"}},"required":["process"]},"handler":app_health}
