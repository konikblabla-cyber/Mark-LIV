"""Windows startup registry inspection."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_registry_startup(parameters=None,**kwargs):
 cmd="Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' -ErrorAction SilentlyContinue | Select-Object *"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No per-user startup entries.")[:12000]
TOOL={"name":"windows_registry_startup","description":"Read-only inspection of the current user's Windows Run startup registry entries.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_registry_startup}
