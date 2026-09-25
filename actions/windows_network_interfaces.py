"""Detailed Windows network interface inventory."""
import platform,subprocess
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def windows_network_interfaces(parameters=None,**kwargs):
 cmd="Get-NetAdapter | Select Name,InterfaceDescription,Status,MacAddress,LinkSpeed,MediaType | Format-Table -AutoSize"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No network adapters.")[:10000]
TOOL={"name":"windows_network_interfaces","description":"Read-only detailed Windows network adapter inventory including status, MAC and link speed.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_network_interfaces}
