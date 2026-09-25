"""Launch an existing Windows executable and wait for its process."""
import os,platform,subprocess,time,psutil
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_process_launch_wait(parameters=None,**kwargs):
 p=parameters or {}; exe=str(p.get("path") or "").strip(); timeout=max(1,min(int(p.get("timeout",30)),120))
 if not exe or not os.path.isfile(exe):return "Executable path does not exist."
 subprocess.Popen([exe],close_fds=True)
 stem=os.path.basename(exe).lower();end=time.time()+timeout
 while time.time()<end:
  for x in psutil.process_iter(["name"]):
   try:
    if (x.info["name"] or "").lower()==stem:return f"Launched and detected {stem} (PID {x.pid})."
   except (psutil.NoSuchProcess,psutil.AccessDenied):pass
  time.sleep(.5)
 return f"Launched {exe}, but process was not detected within {timeout}s."
TOOL={"name":"windows_process_launch_wait","description":"Launch an existing Windows executable and wait for its process to appear.","parameters":{"type":"OBJECT","properties":{"path":{"type":"STRING"},"timeout":{"type":"INTEGER"}},"required":["path"]},"handler":windows_process_launch_wait}
