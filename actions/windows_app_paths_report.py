"""Read-only Windows executable path inventory with publisher metadata."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_app_paths_report(parameters=None,**kwargs):
 p=parameters or {}; pattern=str(p.get("pattern","")).strip(); safe=pattern.replace("'","''")
 filt=f"$_.Name -like '*{safe}*'" if safe else "$true"
 cmd=f"Get-ChildItem 'C:\Program Files','C:\Program Files (x86)' -Filter *.exe -Recurse -ErrorAction SilentlyContinue | Where-Object {{{filt}}} | Select -First 200 FullName,Length,LastWriteTime,VersionInfo | Format-Table -Wrap -AutoSize"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=45,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No executable paths found.")[:20000]
TOOL={"name":"windows_app_paths_report","description":"Read-only inventory of executable paths under Windows Program Files locations, optionally filtered by name.","parameters":{"type":"OBJECT","properties":{"pattern":{"type":"STRING"}}},"handler":windows_app_paths_report}
