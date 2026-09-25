"""Read-only Windows network adapter selection helper."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_network_adapter_select(parameters=None,**kwargs):
 p=parameters or {}; needle=str(p.get("name","")).strip().lower()
 cmd="Get-NetAdapter | Where-Object {$_.Status -eq 'Up'} | Select-Object Name,InterfaceDescription,LinkSpeed,MacAddress,ifIndex | Format-Table -AutoSize"
 if needle:
  safe=needle.replace("'","''");cmd=f"Get-NetAdapter | Where-Object {{$_.Status -eq 'Up' -and ($_.Name -like '*{safe}*' -or $_.InterfaceDescription -like '*{safe}*')}} | Select-Object Name,InterfaceDescription,LinkSpeed,MacAddress,ifIndex | Format-Table -AutoSize"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No matching active network adapter.")[:9000]
TOOL={"name":"windows_network_adapter_select","description":"Read-only lookup of active Windows network adapters, optionally filtered by adapter name.","parameters":{"type":"OBJECT","properties":{"name":{"type":"STRING"}}},"handler":windows_network_adapter_select}
