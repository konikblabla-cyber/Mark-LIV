"""Gracefully close an application by its unique visible window."""
import ctypes,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_app_close_graceful(parameters=None,**kwargs):
 p=parameters or {}; needle=str(p.get("contains") or "").strip().lower()
 if not needle:return "Missing window title text."
 u=ctypes.windll.user32;found=[];W=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_long)
 def cb(h,l):
  if not u.IsWindowVisible(h):return True
  n=u.GetWindowTextLengthW(h);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(h,b,n+1)
  if needle in b.value.lower():found.append((h,b.value))
  return True
 u.EnumWindows(W(cb),0)
 if len(found)!=1:return f"Expected exactly one matching window, found {len(found)}."
 u.PostMessageW(found[0][0],0x0010,0,0)
 return f"Close requested for: '{found[0][1]}'."
TOOL={"name":"windows_app_close_graceful","description":"Gracefully request close for exactly one visible Windows application window; does not force-kill it.","parameters":{"type":"OBJECT","properties":{"contains":{"type":"STRING"}},"required":["contains"]},"handler":windows_app_close_graceful}
