"""Launch a Windows executable and wait for its process to appear."""
import platform,subprocess,time,shlex
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_app_ready(parameters=None,**kwargs):
 p=parameters or {}; command=str(p.get("command","")).strip(); process=str(p.get("process","")).strip(); seconds=max(1,min(int(p.get("seconds",30)),120))
 if not command or not process:return "command and process are required."
 subprocess.Popen(command,shell=True,creationflags=subprocess.CREATE_NO_WINDOW)
 end=time.time()+seconds
 while time.time()<end:
  r=subprocess.run(["tasklist","/FI",f"IMAGENAME eq {process}"],capture_output=True,text=True,timeout=5,creationflags=subprocess.CREATE_NO_WINDOW)
  if process.lower() in r.stdout.lower():return f"Application ready: {process}"
  time.sleep(.5)
 return f"Application did not appear within {seconds}s: {process}"
TOOL={"name":"windows_app_ready","description":"Launch a Windows application and bounded-wait until its process appears.","parameters":{"type":"OBJECT","properties":{"command":{"type":"STRING"},"process":{"type":"STRING"},"seconds":{"type":"INTEGER"}},"required":["command","process"]},"handler":windows_app_ready}
