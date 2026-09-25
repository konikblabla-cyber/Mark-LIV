"""Focus a uniquely matching Windows window and verify foreground focus."""
import ctypes,platform,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_focus_verify(parameters=None,**kwargs):
 p=parameters or {}; needle=str(p.get("contains") or "").strip().lower(); timeout=max(1,min(int(p.get("timeout",5)),20))
 if not needle:return "Missing window title text."
 u=ctypes.windll.user32;matches=[];W=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_long)
 def cb(h,l):
  if u.IsWindowVisible(h):
   n=u.GetWindowTextLengthW(h);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(h,b,n+1)
   if needle in b.value.lower():matches.append(h)
  return True
 u.EnumWindows(W(cb),0)
 if len(matches)!=1:return f"Expected one matching window, found {len(matches)}."
 u.SetForegroundWindow(matches[0]);end=time.time()+timeout
 while time.time()<end:
  if u.GetForegroundWindow()==matches[0]:return f"Focus verified for '{needle}'."
  time.sleep(.1)
 return f"Could not verify focus for '{needle}'."
TOOL={"name":"windows_window_focus_verify","description":"Focus a uniquely matching Windows window and verify foreground focus.","parameters":{"type":"OBJECT","properties":{"contains":{"type":"STRING"},"timeout":{"type":"INTEGER"}},"required":["contains"]},"handler":windows_window_focus_verify}
