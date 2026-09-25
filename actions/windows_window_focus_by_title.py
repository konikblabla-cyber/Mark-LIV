"""Focus a uniquely matched visible Windows window by title."""
import ctypes,platform,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_focus_by_title(parameters=None,**kwargs):
 p=parameters or {}; needle=str(p.get("contains") or "").strip().lower()
 if not needle:return "Missing title text."
 u=ctypes.windll.user32; hits=[]
 W=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_long)
 def cb(h,l):
  if u.IsWindowVisible(h):
   n=u.GetWindowTextLengthW(h);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(h,b,n+1)
   if needle in b.value.lower(): hits.append(h)
  return True
 u.EnumWindows(W(cb),0)
 if len(hits)!=1:return f"Expected exactly one matching window, found {len(hits)}."
 h=hits[0];u.ShowWindow(h,9);u.SetForegroundWindow(h);time.sleep(.15)
 return f"Focused window HWND={h}."
TOOL={"name":"windows_window_focus_by_title","description":"Focus exactly one visible Windows window matching title text.","parameters":{"type":"OBJECT","properties":{"contains":{"type":"STRING"}},"required":["contains"]},"handler":windows_window_focus_by_title}
