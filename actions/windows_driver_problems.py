"""Read-only Windows device-driver problem report."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_driver_problems(parameters=None,**kwargs):
 cmd="Get-CimInstance Win32_PnPEntity | Where-Object {$_.ConfigManagerErrorCode -and $_.ConfigManagerErrorCode -ne 0} | Select Name,PNPDeviceID,ConfigManagerErrorCode,Status | Format-Table -Wrap -AutoSize"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No device-driver problems reported.")[:12000]
TOOL={"name":"windows_driver_problems","description":"Read-only Windows Plug-and-Play device problem report.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_driver_problems}
