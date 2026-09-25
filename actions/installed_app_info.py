"""Windows installed application metadata inspection."""
import platform,subprocess
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def installed_app_info(parameters=None,**kwargs):
 p=parameters or {}; q=str(p.get("name","")).strip()
 if not q:return "Application name required."
 safe_q=q.replace("'","''")
 cmd=f"$roots=@('HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*','HKLM:\\Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*','HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*'); Get-ItemProperty $roots -ErrorAction SilentlyContinue | Where-Object {$_.DisplayName -like '*{safe_q}*'} | Select DisplayName,DisplayVersion,Publisher,InstallDate,InstallLocation,UninstallString | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "Application not found.")[:12000]
TOOL={"name":"installed_app_info","description":"Read-only Windows installed-app metadata lookup by name: version, publisher, install date/location and uninstall command.","parameters":{"type":"OBJECT","properties":{"name":{"type":"STRING"}},"required":["name"]},"handler":installed_app_info}
