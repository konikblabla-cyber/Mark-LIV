"""Read-only Windows application crash summary."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_recent_crashes(parameters=None,**kwargs):
 p=parameters or {}; n=max(1,min(int(p.get("count",20)),50))
 cmd=f"Get-WinEvent -FilterHashtable @{{LogName='Application';ProviderName='Application Error'}} -MaxEvents {n} -ErrorAction SilentlyContinue | Select TimeCreated,Id,Message | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No recent application crashes found.")[:16000]
TOOL={"name":"windows_recent_crashes","description":"Read-only summary of recent Windows Application Error crash events.","parameters":{"type":"OBJECT","properties":{"count":{"type":"INTEGER"}}},"handler":windows_recent_crashes}
