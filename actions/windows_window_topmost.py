"""Set always-on-top state for one visible Windows window."""
import ctypes,platform
from core.permissions import permission_decision
from core import confirm
_TOKEN = object()
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
HWND_TOPMOST=-1;HWND_NOTOPMOST=-2;SWP_NOMOVE=2;SWP_NOSIZE=1;SWP_SHOWWINDOW=0x40
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_topmost(parameters=None,**kwargs):
 if kwargs.get("_permission_token") is not _TOKEN:
  p=dict(parameters or {})
  decision,reason=permission_decision("windows_window_topmost",p)
  if decision=="deny": return f"Permission denied: {reason}"
  if decision=="confirm":
   if confirm.pending_title(): return "There is already a confirmation waiting. Ask the user to answer it first."
   return confirm.request(key="windows_window_topmost",title="Allow JARVIS: windows_window_topmost?",detail=f"{reason}. JARVIS will wait for your confirmation before executing it.",run=lambda: windows_window_topmost(p,_permission_token=_TOKEN))
 p=parameters or {};needle=str(p.get("contains") or "").strip().lower();on=bool(p.get("enabled",True))
 if not needle:return "Missing window title text."
 u=ctypes.windll.user32;found=[]
 def cb(hwnd,lparam):
  if u.IsWindowVisible(hwnd):
   n=u.GetWindowTextLengthW(hwnd);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(hwnd,b,n+1)
   if needle in b.value.lower():found.append((hwnd,b.value))
  return True
 W=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_long);u.EnumWindows(W(cb),0)
 if len(found)!=1:return f"Expected one matching window, found {len(found)}."
 hwnd,title=found[0];ins=HWND_TOPMOST if on else HWND_NOTOPMOST
 ok=u.SetWindowPos(hwnd,ins,0,0,0,0,SWP_NOMOVE|SWP_NOSIZE|SWP_SHOWWINDOW)
 return f"Always-on-top {'enabled' if on else 'disabled'} for '{title}'." if ok else "SetWindowPos failed."
TOOL={"name":"windows_window_topmost","description":"Enable or disable always-on-top for one uniquely matched visible Windows window.","parameters":{"type":"OBJECT","properties":{"contains":{"type":"STRING"},"enabled":{"type":"BOOLEAN"}},"required":["contains"]},"handler":windows_window_topmost}
