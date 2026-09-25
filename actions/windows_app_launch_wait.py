"""Launch an application and wait for its process."""
import platform,subprocess,time,shlex,psutil
def windows_app_launch_wait(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; command=str(p.get("command") or "").strip(); process=str(p.get("process") or "").strip()
 timeout=max(1,min(int(p.get("timeout",30)),120))
 if not command:return "Missing command."
 try: subprocess.Popen(shlex.split(command,posix=False),shell=False)
 except Exception as e:return f"Launch failed: {e}"
 if not process:return "Launched; no process name supplied for readiness check."
 end=time.time()+timeout
 while time.time()<end:
  for x in psutil.process_iter(["name","pid"]):
   try:
    if (x.info["name"] or "").lower()==process.lower():return f"Launched and ready: {process} (PID {x.info['pid']})."
   except (psutil.NoSuchProcess,psutil.AccessDenied):pass
  time.sleep(.4)
 return f"Launched, but {process} was not detected within {timeout}s."
TOOL={"name":"windows_app_launch_wait","description":"Launch a Windows application normally, then wait for its process to appear.","parameters":{"type":"OBJECT","properties":{"command":{"type":"STRING"},"process":{"type":"STRING"},"timeout":{"type":"INTEGER"}},"required":["command"]},"handler":windows_app_launch_wait}
