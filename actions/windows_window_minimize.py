"""Minimize one uniquely matched visible Windows window."""
import ctypes,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
SW_MINIMIZE=6
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_minimize(parameters=None,**kwargs):
 p=parameters or {};needle=str(p.get("contains") or "").strip().lower()
 if not needle:return "Missing window title text."
 u=ctypes.windll.user32;found=[]
 def cb(hwnd,lparam):
  if u.IsWindowVisible(hwnd):
   n=u.GetWindowTextLengthW(hwnd);b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(hwnd,b,n+1)
   if needle in b.value.lower():found.append((hwnd,b.value))
  return True
 W=ctypes.WINFUNCTYPE(ctypes.c_bool,ctypes.c_void_p,ctypes.c_long);u.EnumWindows(W(cb),0)
 if len(found)!=1:return f"Expected one matching window, found {len(found)}."
 hwnd,title=found[0];u.ShowWindow(hwnd,SW_MINIMIZE);return f"Minimized '{title}'."
TOOL={"name":"windows_window_minimize","description":"Minimize one uniquely matched visible Windows window by title text.","parameters":{"type":"OBJECT","properties":{"contains":{"type":"STRING"}},"required":["contains"]},"handler":windows_window_minimize}
