"""Read-only Windows network adapter health."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_network_adapters_health(parameters=None,**kwargs):
 cmd="Get-NetAdapter -IncludeHidden -ErrorAction SilentlyContinue | Select Name,InterfaceDescription,Status,LinkSpeed,MacAddress,Virtual | Format-Table -Wrap -AutoSize"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No network adapters found.")[:12000]
TOOL={"name":"windows_network_adapters_health","description":"Read-only Windows network adapter status, speed and MAC inventory.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_network_adapters_health}
