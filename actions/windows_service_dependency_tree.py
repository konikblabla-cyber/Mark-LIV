"""Read-only Windows service dependency inspection."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_service_dependency_tree(parameters=None,**kwargs):
 p=parameters or {}; name=str(p.get("service","")).strip()
 if not name:return "Service name is required."
 safe=name.replace("'","''"); cmd=f"Get-Service -Name '{safe}' -ErrorAction SilentlyContinue | Select Name,Status,StartType,DependentServices,ServicesDependedOn | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "Service not found.")[:10000]
TOOL={"name":"windows_service_dependency_tree","description":"Read-only Windows service status and dependency inspection.","parameters":{"type":"OBJECT","properties":{"service":{"type":"STRING"}},"required":["service"]},"handler":windows_service_dependency_tree}
