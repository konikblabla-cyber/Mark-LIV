"""Wait for a Windows process to become ready."""
import platform,subprocess,time
def windows_app_wait(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; name=str(p.get("process","")).strip(); timeout=max(.5,min(float(p.get("timeout",20)),60))
 if not name:return "Process executable name is required."
 base=name.rsplit(".",1)[0].replace("'","''"); end=time.time()+timeout
 while time.time()<end:
  ps=f"Get-Process -Name '{base}' -ErrorAction SilentlyContinue | Select-Object -First 1 Id,ProcessName,Responding | ConvertTo-Json -Compress"
  r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",ps],capture_output=True,text=True,timeout=5,creationflags=subprocess.CREATE_NO_WINDOW)
  if r.stdout.strip(): return "Ready: "+r.stdout.strip()
  time.sleep(.5)
 return f"{name} did not appear within {timeout:g}s."
TOOL={"name":"windows_app_wait","description":"Wait briefly for a named Windows process to appear, useful after launching an application.","parameters":{"type":"OBJECT","properties":{"process":{"type":"STRING"},"timeout":{"type":"NUMBER"}},"required":["process"]},"handler":windows_app_wait}
