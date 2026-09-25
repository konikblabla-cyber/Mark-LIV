"""Read-only Windows failed-service diagnosis."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_service_failures(parameters=None,**kwargs):
 cmd="Get-CimInstance Win32_Service | Where-Object {$_.State -ne 'Running' -and $_.StartMode -eq 'Auto'} | Select Name,DisplayName,State,StartMode,StartName,PathName | Format-Table -Wrap -AutoSize"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No failed/stopped automatic services found.")[:16000]
TOOL={"name":"windows_service_failures","description":"Read-only Windows report of automatic services that are currently not running.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_service_failures}
