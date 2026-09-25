"""Windows physical display inventory."""
import platform,subprocess
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def windows_displays_info(parameters=None,**kwargs):
 cmd="Get-CimInstance Win32_DesktopMonitor | Select Name,MonitorType,ScreenWidth,ScreenHeight,PNPDeviceID,Status | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No display information.")[:10000]
TOOL={"name":"windows_displays_info","description":"Read-only Windows physical display inventory with resolution and device information when exposed by WMI.","parameters":{"type":"OBJECT","properties":{}},"handler=windows_displays_info}
