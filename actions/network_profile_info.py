"""Windows network profile inspection."""
import platform,subprocess
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def network_profile_info(parameters=None,**kwargs):
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command","Get-NetConnectionProfile | Select Name,InterfaceAlias,NetworkCategory,IPv4Connectivity,IPv6Connectivity | Format-Table -AutoSize"],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No network profiles.")[:10000]
TOOL={"name":"network_profile_info","description":"Read-only Windows network profile and connectivity information.","parameters":{"type":"OBJECT","properties":{}},"handler":network_profile_info}
