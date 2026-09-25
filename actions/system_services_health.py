"""Windows service health overview for Mark-LIV."""
import platform,subprocess
def system_services_health(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; a=str(p.get("action","failed")).lower().strip()
 cmds={"failed":"Get-Service | Where-Object {$_.Status -eq 'Stopped' -and $_.StartType -eq 'Automatic'} | Select Name,DisplayName,Status,StartType | Format-Table -AutoSize","running":"Get-Service | Where-Object {$_.Status -eq 'Running'} | Measure-Object","summary":"Get-Service | Group-Object Status | Select Name,Count | Format-Table -AutoSize"}
 if a not in cmds:return "Use failed, running or summary."
 try:
  r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmds[a]],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 except (subprocess.TimeoutExpired,OSError) as e:return f"Service health check failed: {e}"
 return (r.stdout or r.stderr or "No service data.")[:10000]
TOOL={"name":"system_services_health","description":"Windows-only service health overview: stopped automatic services, running-service count, or status summary. Read-only.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}},"required":["action"]},"handler":system_services_health}
