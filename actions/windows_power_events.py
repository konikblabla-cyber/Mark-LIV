"""Read-only recent Windows power-management events."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_power_events(parameters=None,**kwargs):
 p=parameters or {}; n=max(1,min(int(p.get("count",30)),100))
 cmd=f"Get-WinEvent -FilterHashtable @{{LogName='System';ProviderName='Microsoft-Windows-Kernel-Power'}} -MaxEvents {n} -ErrorAction SilentlyContinue | Select TimeCreated,Id,LevelDisplayName,Message | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No recent power events found.")[:18000]
TOOL={"name":"windows_power_events","description":"Read-only recent Windows Kernel-Power event report for sleep, resume and power-related diagnostics.","parameters":{"type":"OBJECT","properties":{"count":{"type":"INTEGER"}}},"handler":windows_power_events}
