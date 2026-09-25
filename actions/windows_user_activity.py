"""Read-only Windows user/session activity summary."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_user_activity(parameters=None,**kwargs):
 ps="$p=Get-Process | Where-Object {$_.MainWindowTitle}; $p | Sort-Object StartTime -Descending | Select-Object -First 50 Id,ProcessName,StartTime,MainWindowTitle | Format-Table -Wrap -AutoSize"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",ps],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No active user applications found.")[:14000]
TOOL={"name":"windows_user_activity","description":"Read-only list of recent visible Windows applications with process IDs and window titles.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_user_activity}
