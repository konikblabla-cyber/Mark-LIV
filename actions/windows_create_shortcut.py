"""Create a Windows shortcut."""
import os,platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_create_shortcut(parameters=None,**kwargs):
 p=parameters or {};target=str(p.get("target","")).strip();link=str(p.get("shortcut","")).strip()
 if not target or not link:return "Missing target or shortcut."
 if not os.path.exists(target):return f"Target not found: {target}"
 ps=f"$s=(New-Object -ComObject WScript.Shell).CreateShortcut('{link.replace("'","''")}');$s.TargetPath='{target.replace("'","''")}';$s.Save()"
 subprocess.run(["powershell","-NoProfile","-Command",ps],check=True,creationflags=0x08000000)
 return f"Created shortcut: {link}"
TOOL={"name":"windows_create_shortcut","description":"Create a Windows .lnk shortcut to an existing target.","parameters":{"type":"OBJECT","properties":{"target":{"type":"STRING"},"shortcut":{"type":"STRING"}},"required":["target","shortcut"]},"handler=windows_create_shortcut}
