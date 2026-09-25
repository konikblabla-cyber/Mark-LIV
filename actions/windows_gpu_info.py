"""Windows GPU inventory."""
import platform,subprocess
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def windows_gpu_info(parameters=None,**kwargs):
 cmd="Get-CimInstance Win32_VideoController | Select Name,DriverVersion,AdapterRAM,VideoModeDescription,Status | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No GPU information.")[:10000]
TOOL={"name":"windows_gpu_info","description":"Read-only Windows GPU model, driver, memory and display-mode information.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_gpu_info}
