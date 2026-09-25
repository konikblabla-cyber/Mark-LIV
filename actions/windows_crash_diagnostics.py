"""Read-only Windows crash diagnostics."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_crash_diagnostics(parameters=None,**kwargs):
 p=parameters or {}; n=max(1,min(int(p.get("count",20)),50))
 cmd=f"Get-WinEvent -FilterHashtable @{{LogName='System';Level=2}} -MaxEvents {n} -ErrorAction SilentlyContinue | Select TimeCreated,Id,ProviderName,Message | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No recent system errors.")[:16000]
TOOL={"name":"windows_crash_diagnostics","description":"Read-only recent Windows System event errors useful for diagnosing crashes and hardware/service failures.","parameters":{"type":"OBJECT","properties":{"count":{"type":"INTEGER"}}},"handler":windows_crash_diagnostics}
