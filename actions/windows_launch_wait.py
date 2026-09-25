"""Launch a Windows application and wait for its process."""
import platform,subprocess,time,psutil
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_launch_wait(parameters=None,**kwargs):
 p=parameters or {}; command=str(p.get("command") or "").strip(); process=str(p.get("process") or "").strip()
 timeout=max(1,min(int(p.get("timeout",30)),120))
 if not command:return "Missing command."
 try: subprocess.Popen(command,shell=True)
 except Exception as e:return f"Launch failed: {e}"
 if not process:return f"Launched: {command}"
 end=time.time()+timeout
 while time.time()<end:
  for x in psutil.process_iter(["name","pid"]):
   try:
    if (x.info["name"] or "").lower()==process.lower(): return f"Launched and ready: {process} (PID {x.info['pid']})."
   except (psutil.NoSuchProcess,psutil.AccessDenied):pass
  time.sleep(.5)
 return f"Launched '{command}', but '{process}' was not detected within {timeout}s."
TOOL={"name":"windows_launch_wait","description":"Launch a Windows application and optionally wait until its process appears.","parameters":{"type":"OBJECT","properties":{"command":{"type":"STRING"},"process":{"type":"STRING"},"timeout":{"type":"INTEGER"}},"required":["command"]},"handler":windows_launch_wait}
