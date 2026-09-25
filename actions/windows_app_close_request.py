"""Request graceful close for one uniquely matched Windows application."""
import ctypes,platform,time
WM_CLOSE=0x0010
def windows_app_close_request(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; title=str(p.get("contains") or "").strip().lower()
 if not title:return "Missing window title text."
 u=ctypes.windll.user32;found=[]
 def cb(hwnd,_):
  if u.IsWindowVisible(hwnd):
   n=u.GetWindowTextLengthW(hwnd);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(hwnd,b,n+1)
   if title in b.value.lower():found.append(hwnd)
  return True
 W=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_long);u.EnumWindows(W(cb),0)
 if len(found)!=1:return f"Expected exactly one matching window; found {len(found)}."
 u.PostMessageW(found[0],WM_CLOSE,0,0);time.sleep(.2);return "Close request sent."
TOOL={"name":"windows_app_close_request","description":"Gracefully request closing one uniquely matched Windows window without force-killing the process.","parameters":{"type":"OBJECT","properties":{"contains":{"type":"STRING"}},"required":["contains"]},"handler":windows_app_close_request}
