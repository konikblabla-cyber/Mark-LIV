"""Windows startup inventory."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_startup_inventory(parameters=None,**kwargs):
 cmd="Get-CimInstance Win32_StartupCommand | Select Name,Command,Location,User | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No startup entries found.")[:20000]
TOOL={"name":"windows_startup_inventory","description":"Read-only complete Windows startup command inventory.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_startup_inventory}
