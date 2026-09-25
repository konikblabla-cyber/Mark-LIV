"""Move and resize a uniquely matched visible Windows window."""
import ctypes,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_move_resize(parameters=None,**kwargs):
 p=parameters or {}; needle=str(p.get("contains") or "").strip().lower()
 if not needle:return "Missing window title text."
 vals=[p.get(k) for k in ("x","y","width","height")]
 if any(v is None for v in vals):return "x, y, width and height are required."
 x,y,w,h=[int(v) for v in vals]
 if w<50 or h<50:return "Window size must be at least 50x50."
 u=ctypes.windll.user32; found=[]
 def cb(hwnd,lparam):
  if u.IsWindowVisible(hwnd):
   n=u.GetWindowTextLengthW(hwnd);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(hwnd,b,n+1)
   if needle in b.value.lower():found.append((hwnd,b.value))
  return True
 W=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_long);u.EnumWindows(W(cb),0)
 if len(found)!=1:return f"Expected one matching window, found {len(found)}."
 hwnd,title=found[0]
 if not u.SetWindowPos(hwnd,0,x,y,w,h,0x0040):return "SetWindowPos failed."
 return f"Moved/resized '{title}' to {x},{y} {w}x{h}."
TOOL={"name":"windows_window_move_resize","description":"Move and resize one uniquely matched visible Windows window.","parameters":{"type":"OBJECT","properties":{"contains":{"type":"STRING"},"x":{"type":"INTEGER"},"y":{"type":"INTEGER"},"width":{"type":"INTEGER"},"height":{"type":"INTEGER"}},"required":["contains","x","y","width","height"]},"handler":windows_window_move_resize}
