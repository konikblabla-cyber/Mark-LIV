"""Request close for a uniquely matched Windows window."""
import ctypes,platform
WM_CLOSE=0x0010
def windows_app_close(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; needle=str(p.get("contains") or "").strip().lower()
 if not needle:return "Missing window title text."
 u=ctypes.windll.user32;matches=[];W=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_long)
 def cb(h,l):
  if u.IsWindowVisible(h):
   n=u.GetWindowTextLengthW(h);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(h,b,n+1)
   if needle in b.value.lower():matches.append((h,b.value))
  return True
 u.EnumWindows(W(cb),0)
 if len(matches)!=1:return f"Expected exactly one matching window, found {len(matches)}."
 u.PostMessageW(matches[0][0],WM_CLOSE,0,0)
 return f"Close requested: '{matches[0][1]}'."
TOOL={"name":"windows_app_close","description":"Request close for exactly one visible Windows window matched by title text; no force kill.","parameters":{"type":"OBJECT","properties":{"contains":{"type":"STRING"}},"required":["contains"]},"handler":windows_app_close}
