"""Launch a Windows program and wait until its process appears."""
import platform,subprocess,time,psutil

def windows_launch_and_wait(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; cmd=str(p.get("command") or "").strip(); proc=str(p.get("process") or "").strip()
 timeout=max(1,min(int(p.get("timeout",30)),120))
 if not cmd or not proc:return "command and process are required."
 subprocess.Popen(cmd,shell=True,creationflags=subprocess.CREATE_NO_WINDOW)
 end=time.time()+timeout
 while time.time()<end:
  for x in psutil.process_iter(["name","pid"]):
   try:
    if (x.info["name"] or "").lower()==proc.lower(): return f"Launched and ready: {proc} (PID {x.info['pid']})."
   except (psutil.NoSuchProcess,psutil.AccessDenied): pass
  time.sleep(.4)
 return f"Process did not appear within {timeout}s: {proc}"
TOOL={"name":"windows_launch_and_wait","description":"Launch a Windows application and wait for its process to appear.","parameters":{"type":"OBJECT","properties":{"command":{"type":"STRING"},"process":{"type":"STRING"},"timeout":{"type":"INTEGER"}},"required":["command","process"]},"handler":windows_launch_and_wait}
