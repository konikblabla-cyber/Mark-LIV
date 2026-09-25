"""Launch a Windows application and optionally wait for its window."""
import platform,subprocess,time,ctypes
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_app_launch_and_focus(parameters=None,**kwargs):
 p=parameters or {}; command=str(p.get("command") or "").strip(); title=str(p.get("window_contains") or "").strip().lower()
 if not command:return "Missing application command."
 subprocess.Popen(command, shell=True)
 if not title:return f"Launched: {command}"
 u=ctypes.windll.user32; end=time.time()+max(1,min(int(p.get("timeout",20)),60))
 while time.time()<end:
  h=u.GetForegroundWindow(); n=u.GetWindowTextLengthW(h); b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(h,b,n+1)
  if title in b.value.lower(): return f"Launched and focused window: '{b.value}'."
  time.sleep(.25)
 return f"Launched '{command}', but target window did not become active within timeout."
TOOL={"name":"windows_app_launch_and_focus","description":"Launch a Windows application and optionally wait for a matching foreground window.","parameters":{"type":"OBJECT","properties":{"command":{"type":"STRING"},"window_contains":{"type":"STRING"},"timeout":{"type":"INTEGER"}},"required":["command"]},"handler":windows_app_launch_and_focus}
