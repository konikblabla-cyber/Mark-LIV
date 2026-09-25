"""Read-only Windows boot diagnostics."""
import platform,subprocess
def windows_boot_diagnostics(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 cmd="Get-WinEvent -FilterHashtable @{LogName='System';Id=12,13,6005,6006} -MaxEvents 30 -ErrorAction SilentlyContinue | Select TimeCreated,Id,ProviderName,Message | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No boot events found.")[:14000]
TOOL={"name":"windows_boot_diagnostics","description":"Read-only recent Windows boot and shutdown event diagnostics.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_boot_diagnostics}
