"""Windows recent system error summary."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_recent_errors(parameters=None,**kwargs):
 p=parameters or {}; n=max(1,min(int(p.get("limit",20)),100))
 cmd=f"Get-WinEvent -FilterHashtable @{{LogName='System'; Level=2}} -MaxEvents {n} -ErrorAction SilentlyContinue | Select TimeCreated,ProviderName,Id,Message | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No recent system errors found.")[:16000]
TOOL={"name":"windows_recent_errors","description":"Read-only recent Windows System event errors for troubleshooting.","parameters":{"type":"OBJECT","properties":{"limit":{"type":"INTEGER"}}},"handler":windows_recent_errors}
