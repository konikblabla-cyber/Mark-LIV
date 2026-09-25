"""Windows Start menu control."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_start_menu(parameters=None,**kwargs):
 p=parameters or {}; action=str(p.get("action","open")).lower()
 keys={"open":["win"],"close":["esc"],"search":["win","s"]}
 if action not in keys:return "Supported actions: open, close, search."
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command","$ws=New-Object -ComObject WScript.Shell; "+("; ".join(f"$ws.SendKeys('{{{k.upper()}}}')" for k in keys[action]))],capture_output=True,text=True,timeout=10,creationflags=subprocess.CREATE_NO_WINDOW)
 return "Start menu action completed." if r.returncode==0 else (r.stderr or "Start menu action failed.")
TOOL={"name":"windows_start_menu","description":"Open, close, or focus Windows Start/search using normal keyboard input.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING","enum":["open","close","search"]}}},"handler":windows_start_menu}
