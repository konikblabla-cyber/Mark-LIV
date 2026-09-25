"""Wait until a target window becomes foreground."""
import ctypes,platform,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_activate_wait(parameters=None,**kwargs):
 p=parameters or {}; needle=str(p.get("contains") or "").strip().lower()
 timeout=max(1,min(int(p.get("timeout",30)),120))
 if not needle:return "Missing window title text."
 u=ctypes.windll.user32; end=time.time()+timeout
 while time.time()<end:
  hwnd=u.GetForegroundWindow(); n=u.GetWindowTextLengthW(hwnd); b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(hwnd,b,n+1)
  if needle in b.value.lower(): return f"Window active: '{b.value}'."
  time.sleep(.25)
 return f"Window did not become active within {timeout}s: {needle}"
TOOL={"name":"windows_window_activate_wait","description":"Wait for a Windows window with matching title text to become the foreground window.","parameters":{"type":"OBJECT","properties":{"contains":{"type":"STRING"},"timeout":{"type":"INTEGER"}},"required":["contains"]},"handler":windows_window_activate_wait}
