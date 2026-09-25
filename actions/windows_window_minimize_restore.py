"""Directly minimize or restore one uniquely matched Windows window."""
import ctypes,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_minimize_restore(parameters=None,**kwargs):
 p=parameters or {}; needle=str(p.get("contains") or "").strip().lower(); action=str(p.get("action","minimize")).lower()
 if not needle or action not in ("minimize","restore"):return "Provide window text and action minimize/restore."
 u=ctypes.windll.user32;hits=[]
 def cb(h,_):
  if u.IsWindowVisible(h):
   n=u.GetWindowTextLengthW(h);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(h,b,n+1)
   if needle in b.value.lower():hits.append((h,b.value))
  return True
 W=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_long);u.EnumWindows(W(cb),0)
 if len(hits)!=1:return f"Expected one matching window, found {len(hits)}."
 u.ShowWindow(hits[0][0],6 if action=="minimize" else 9)
 return f"{action.title()}d: '{hits[0][1]}'."
TOOL={"name":"windows_window_minimize_restore","description":"Minimize or restore one uniquely matched visible Windows window.","parameters":{"type":"OBJECT","properties":{"contains":{"type":"STRING"},"action":{"type":"STRING"}},"required":["contains"]},"handler":windows_window_minimize_restore}
