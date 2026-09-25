"""Windows process auto-start inspection."""
import platform,subprocess
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def process_autostart(parameters=None,**kwargs):
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command","Get-CimInstance Win32_StartupCommand | Select Name,Command,Location,User | Format-Table -AutoSize"],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No startup entries.")[:12000]
TOOL={"name":"process_autostart","description":"Read-only Windows startup inventory showing startup item name, command, location and user.","parameters":{"type":"OBJECT","properties":{}},"handler":process_autostart}
