"""Windows display state inventory."""
import platform,subprocess
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def windows_display_state(parameters=None,**kwargs):
 cmd="Get-CimInstance Win32_VideoController | Select Name,DriverVersion,VideoModeDescription,CurrentHorizontalResolution,CurrentVerticalResolution,AdapterRAM | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No display adapter data.")[:10000]
TOOL={"name":"windows_display_state","description":"Read-only Windows display/GPU mode inventory with driver and current resolution information.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_display_state}
