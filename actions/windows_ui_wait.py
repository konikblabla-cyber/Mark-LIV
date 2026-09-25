"""Wait for a Windows UI condition."""
import ctypes,platform,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_wait(parameters=None,**kwargs):
 p=parameters or {}; needle=str(p.get("title_contains") or "").strip().lower(); timeout=max(1,min(int(p.get("timeout",30)),120))
 if not needle:return "Missing title_contains."
 u=ctypes.windll.user32;end=time.time()+timeout
 while time.time()<end:
  h=u.GetForegroundWindow();n=u.GetWindowTextLengthW(h);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(h,b,n+1)
  if needle in b.value.lower():return f"Condition met: '{b.value}'."
  time.sleep(.25)
 return f"Condition not met after {timeout}s."
TOOL={"name":"windows_ui_wait","description":"Bounded wait until foreground Windows UI title contains requested text.","parameters":{"type":"OBJECT","properties":{"title_contains":{"type":"STRING"},"timeout":{"type":"INTEGER"}},"required":["title_contains"]},"handler":windows_ui_wait}
