"""Windows installed application metadata inspection."""
import platform,subprocess
def installed_app_info(parameters=None,**kwargs):
 if platform.system()!="Windows": return "installed_app_info is available only on Windows."
 p=parameters or {}; q=str(p.get("name","")).strip()
 if not q:return "Application name required."
 safe_q=q.replace("'","''")
 ps_roots = r"""HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*,HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*,HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*"""
 cmd=f"$roots=@({','.join(repr(x) for x in ps_roots.split(','))}); Get-ItemProperty $roots -ErrorAction SilentlyContinue | Where-Object {{$_.DisplayName -like '*{safe_q}*'}} | Select DisplayName,DisplayVersion,Publisher,InstallDate,InstallLocation,UninstallString | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "Application not found.")[:12000]
TOOL={"name":"installed_app_info","description":"Read-only Windows installed-app metadata lookup by name: version, publisher, install date/location and uninstall command.","parameters":{"type":"OBJECT","properties":{"name":{"type":"STRING"}},"required":["name"]},"handler":installed_app_info}
