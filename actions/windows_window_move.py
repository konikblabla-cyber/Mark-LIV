"""Move and resize a uniquely matched Windows window."""
import ctypes,platform
from core.permissions import permission_decision
from core import confirm
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_move(parameters=None,**kwargs):
 if not kwargs.get("_permission_token"):
  p=dict(parameters or {});d,r=permission_decision("windows_window_move",p)
  if d=="deny":return f"Permission denied: {r}"
  if d=="confirm":return confirm.request(key="windows_window_move",title="Allow JARVIS: windows_window_move?",detail=f"{r}. Waiting for your confirmation.",run=lambda:windows_window_move(p,_permission_token=True))
 p=parameters or {}; needle=str(p.get("contains") or "").strip().lower()
 try:x=int(p.get("x",0));y=int(p.get("y",0));w=int(p.get("width",800));h=int(p.get("height",600))
 except ValueError:return "Invalid geometry."
 if not needle:return "Missing window title text."
 x=max(-10000,min(x,10000));y=max(-10000,min(y,10000));w=max(100,min(w,10000));h=max(100,min(h,10000))
 u=ctypes.windll.user32;matches=[];W=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_long)
 def cb(hw,l):
  if u.IsWindowVisible(hw):
   n=u.GetWindowTextLengthW(hw);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(hw,b,n+1)
   if needle in b.value.lower():matches.append((hw,b.value))
  return True
 u.EnumWindows(W(cb),0)
 if len(matches)!=1:return f"Expected one matching window, found {len(matches)}."
 hw,title=matches[0];u.MoveWindow(hw,x,y,w,h,True);return f"Moved '{title}' to {x},{y} size {w}x{h}."
TOOL={"name":"windows_window_move","description":"Move and resize one uniquely matched Windows window.","parameters":{"type":"OBJECT","properties":{"contains":{"type":"STRING"},"x":{"type":"INTEGER"},"y":{"type":"INTEGER"},"width":{"type":"INTEGER"},"height":{"type":"INTEGER"}},"required":["contains","x","y","width","height"]},"handler":windows_window_move}
