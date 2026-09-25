"""Launch a Windows executable and wait until its process appears."""
import platform,subprocess,time,psutil
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_app_launch_ready(parameters=None,**kwargs):
 p=parameters or {};cmd=str(p.get("command") or p.get("path") or "").strip();timeout=max(1,min(int(p.get("timeout",30)),120))
 if not cmd:return "Missing command or executable path."
 try: subprocess.Popen(cmd,shell=False)
 except Exception as e:return f"Launch failed: {e}"
 name=cmd.replace("\\","/").rsplit("/",1)[-1].lower()
 end=time.time()+timeout
 while time.time()<end:
  for x in psutil.process_iter(["name","pid"]):
   try:
    if (x.info["name"] or "").lower()==name:return f"Launched and ready: {x.info['name']} (PID {x.info['pid']})."
   except (psutil.NoSuchProcess,psutil.AccessDenied):pass
  time.sleep(.5)
 return f"Launched, but process '{name}' was not detected within {timeout}s."
TOOL={"name":"windows_app_launch_ready","description":"Launch a Windows executable normally and wait for its process to appear.","parameters":{"type":"OBJECT","properties":{"command":{"type":"STRING"},"path":{"type":"STRING"},"timeout":{"type":"INTEGER"}}},"handler":windows_app_launch_ready}
