"""Windows recent event log inspection."""
import platform,subprocess
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def eventlog_recent(parameters=None,**kwargs):
 p=parameters or {}; log=str(p.get("log","System")); n=max(1,min(int(p.get("count",20)),100))
 safe=log if log in {"System","Application","Security"} else "System"
 cmd=f"Get-WinEvent -LogName '{safe}' -MaxEvents {n} | Select TimeCreated,Id,LevelDisplayName,ProviderName,Message | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No events.")[:16000]
TOOL={"name":"eventlog_recent","description":"Read-only Windows recent event inspection for System, Application or Security logs.","parameters":{"type":"OBJECT","properties":{"log":{"type":"STRING"},"count":{"type":"INTEGER"}},"required":["log"]},"handler=eventlog_recent}
