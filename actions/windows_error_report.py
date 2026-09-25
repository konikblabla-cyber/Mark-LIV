"""Windows application error event report."""
import platform,subprocess
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def windows_error_report(parameters=None,**kwargs):
 p=parameters or {}; n=max(1,min(int(p.get("count",30)),100))
 cmd=f"Get-WinEvent -FilterHashtable @{{LogName='Application';Level=2}} -MaxEvents {n} -ErrorAction SilentlyContinue | Select TimeCreated,Id,ProviderName,Message | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No recent application errors.")[:16000]
TOOL={"name":"windows_error_report","description":"Read-only Windows Application event-log error report for recent application failures.","parameters":{"type":"OBJECT","properties":{"count":{"type":"INTEGER"}},"required":["count"]},"handler=windows_error_report}
