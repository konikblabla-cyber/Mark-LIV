"""Wait for any visible Windows window matching title text."""
import platform,time,ctypes
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_wait_for_window(parameters=None,**kwargs):
 p=parameters or {}; needle=str(p.get("contains") or "").strip().lower(); timeout=max(1,min(int(p.get("timeout",30)),120))
 if not needle:return "Missing title text."
 u=ctypes.windll.user32; end=time.time()+timeout
 while time.time()<end:
  hit=[]
  def cb(hwnd,l):
   if u.IsWindowVisible(hwnd):
    n=u.GetWindowTextLengthW(hwnd);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(hwnd,b,n+1)
    if needle in b.value.lower():hit.append(b.value)
   return True
  u.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_long)(cb),0)
  if hit:return f"Window found: '{hit[0]}'."
  time.sleep(.4)
 return f"Window not found within {timeout}s: {needle}"
TOOL={"name":"windows_wait_for_window","description":"Wait for a visible Windows window whose title contains given text.","parameters":{"type":"OBJECT","properties":{"contains":{"type":"STRING"},"timeout":{"type":"INTEGER"}},"required":["contains"]},"handler":windows_wait_for_window}
