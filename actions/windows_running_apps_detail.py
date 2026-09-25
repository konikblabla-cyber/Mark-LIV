"""Read-only detailed inventory of visible Windows applications."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_running_apps_detail(parameters=None,**kwargs):
 p=parameters or {}; n=max(1,min(int(p.get("count",50)),150))
 cmd=f"Get-Process | Where-Object {{$_.MainWindowTitle}} | Sort-Object CPU -Descending | Select-Object -First {n} Id,ProcessName,CPU,WorkingSet64,StartTime,MainWindowTitle,Path | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=25,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No visible applications found.")[:22000]
TOOL={"name":"windows_running_apps_detail","description":"Read-only detailed inventory of visible Windows apps including CPU, memory, start time and executable path.","parameters":{"type":"OBJECT","properties":{"count":{"type":"INTEGER"}}},"handler":windows_running_apps_detail}
