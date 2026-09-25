"""Bounded wait for a Windows process to exit."""
import platform,subprocess,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_process_wait(parameters=None,**kwargs):
 p=parameters or {}; name=str(p.get("process","")).strip(); timeout=max(.5,min(float(p.get("timeout",60)),120))
 if not name:return "Process executable name is required."
 base=name.rsplit(".",1)[0].replace("'","''"); end=time.time()+timeout
 while time.time()<end:
  ps=f"Get-Process -Name '{base}' -ErrorAction SilentlyContinue | Select-Object -First 1 Id"
  r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",ps],capture_output=True,text=True,timeout=5,creationflags=subprocess.CREATE_NO_WINDOW)
  if not r.stdout.strip(): return f"{name} exited."
  time.sleep(.5)
 return f"{name} is still running after {timeout:g}s."
TOOL={"name":"windows_process_wait","description":"Wait briefly for a named Windows process to exit.","parameters":{"type":"OBJECT","properties":{"process":{"type":"STRING"},"timeout":{"type":"NUMBER"}},"required":["process"]},"handler":windows_process_wait}
