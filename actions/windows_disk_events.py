"""Windows storage event diagnostics."""
import platform,subprocess
def windows_disk_events(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; n=max(1,min(int(p.get("limit",20)),100))
 cmd=f"Get-WinEvent -FilterHashtable @{{LogName='System'; ProviderName='disk'}} -MaxEvents {n} -ErrorAction SilentlyContinue | Select TimeCreated,Id,LevelDisplayName,Message | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No disk events found.")[:16000]
TOOL={"name":"windows_disk_events","description":"Read-only Windows disk-provider event diagnostics for storage troubleshooting.","parameters":{"type":"OBJECT","properties":{"limit":{"type":"INTEGER"}}},"handler":windows_disk_events}
