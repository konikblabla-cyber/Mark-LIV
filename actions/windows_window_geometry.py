"""Read-only Windows window geometry inspector."""
import platform,ctypes
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_geometry(parameters=None,**kwargs):
 p=parameters or {}; title=str(p.get("title","")).strip().lower()
 if not title:return "Window title is required."
 u=ctypes.windll.user32; found=[]
 class R(ctypes.Structure):_fields_=[("l",ctypes.c_long),("t",ctypes.c_long),("r",ctypes.c_long),("b",ctypes.c_long)]
 def cb(hwnd,lparam):
  if u.IsWindowVisible(hwnd):
   n=u.GetWindowTextLengthW(hwnd);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(hwnd,b,n+1)
   if title in b.value.lower():found.append((hwnd,b.value))
  return True
 u.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_void_p)(cb),0)
 out=[]
 for h,t in found[:10]:
  r=R();u.GetWindowRect(h,ctypes.byref(r));out.append(f"{t}: x={r.l} y={r.t} w={r.r-r.l} h={r.b-r.t}")
 return "\n".join(out) or "Window not found."
TOOL={"name":"windows_window_geometry","description":"Read-only visible Windows window position and size by title.","parameters":{"type":"OBJECT","properties":{"title":{"type":"STRING"}},"required":["title"]},"handler":windows_window_geometry}
