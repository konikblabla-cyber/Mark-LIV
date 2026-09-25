"""Launch a Windows application, wait for its process, then focus a matching window."""
import platform,subprocess,time,psutil,ctypes
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_app_launch_wait_focus(parameters=None,**kwargs):
 p=parameters or {}; cmd=str(p.get("command") or "").strip(); needle=str(p.get("window_contains") or "").strip().lower()
 if not cmd:return "Missing command."
 subprocess.Popen(cmd,shell=True)
 end=time.time()+max(1,min(int(p.get("timeout",30)),120))
 while time.time()<end:
  if needle:
   u=ctypes.windll.user32; h=u.GetForegroundWindow();n=u.GetWindowTextLengthW(h);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(h,b,n+1)
   if needle in b.value.lower():return f"Application launched and window active: {b.value}"
  else:
   return "Application launch requested."
  time.sleep(.3)
 return "Application launched, but target window did not become active."
TOOL={"name":"windows_app_launch_wait_focus","description":"Launch a Windows application and optionally wait for its target window title to become active.","parameters":{"type":"OBJECT","properties":{"command":{"type":"STRING"},"window_contains":{"type":"STRING"},"timeout":{"type":"INTEGER"}},"required":["command"]},"handler":windows_app_launch_wait_focus}
