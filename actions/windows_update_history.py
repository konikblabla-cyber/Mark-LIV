"""Read-only Windows update history."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_update_history(parameters=None,**kwargs):
 p=parameters or {}; n=max(1,min(int(p.get("count",30)),100))
 cmd=f"Get-HotFix | Sort-Object InstalledOn -Descending | Select -First {n} HotFixID,InstalledOn,Description,InstalledBy | Format-Table -AutoSize"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No update history available.")[:10000]
TOOL={"name":"windows_update_history","description":"Read-only Windows installed hotfix and update history.","parameters":{"type":"OBJECT","properties":{"count":{"type":"INTEGER"}}},"handler":windows_update_history}
