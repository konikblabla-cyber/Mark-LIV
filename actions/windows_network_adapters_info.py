"""Windows network adapter inventory."""
import platform,subprocess
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def windows_network_adapters_info(parameters=None,**kwargs):
 cmd="Get-NetAdapter -ErrorAction SilentlyContinue | Select Name,InterfaceDescription,Status,MacAddress,LinkSpeed,MediaType | Format-Table -AutoSize"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No network adapters.")[:10000]
TOOL={"name":"windows_network_adapters_info","description":"Read-only Windows network-adapter inventory with status, MAC address and link speed.","parameters":{"type":"OBJECT","properties":{}},"handler=windows_network_adapters_info}
