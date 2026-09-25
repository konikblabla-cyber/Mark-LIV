"""Windows network profile inspection."""
import platform,subprocess

def network_profile_info(parameters=None,**kwargs):
    if platform.system()!="Windows":
        return "Windows-only action."
    try:
        r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command","Get-NetConnectionProfile | Select Name,InterfaceAlias,NetworkCategory,IPv4Connectivity,IPv6Connectivity | Format-Table -AutoSize"],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
    except (subprocess.TimeoutExpired,OSError) as e:
        return f"Network profile inspection failed: {e}"
    return (r.stdout or r.stderr or "No network profiles.")[:10000]

TOOL={"name":"network_profile_info","description":"Read-only Windows network profile and connectivity information.","parameters":{"type":"OBJECT","properties":{}},"handler":network_profile_info}
