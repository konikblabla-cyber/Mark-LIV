"""Windows power-state inspection."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_power_status(parameters=None,**kwargs):
 cmd="powercfg /getactivescheme; powercfg /a"
 r=subprocess.run(["cmd.exe","/c",cmd],capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No power data.")[:8000]
TOOL={"name":"windows_power_status","description":"Read-only Windows power plan and available sleep-state information.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_power_status}
