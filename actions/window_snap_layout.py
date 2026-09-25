"""Windows snap-style window arrangement for Mark-LIV."""
import platform,ctypes
from ctypes import wintypes
u=ctypes.windll.user32
def window_snap_layout(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; mode=str(p.get("mode","left")).lower(); title=str(p.get("title","")).strip()
 targets=[]
 if title:
  n=len(title); 
  for _ in [0]:
   def cb(hwnd,_l):
    if u.IsWindowVisible(hwnd):
     b=ctypes.create_unicode_buffer(n+512);u.GetWindowTextW(hwnd,b,len(b))
     if title.casefold() in b.value.casefold():targets.append(hwnd)
    return True
   u.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool,wintypes.HWND,wintypes.LPARAM)(cb),0)
 if not targets:return "Window not found."
 hwnd=targets[0]; sw=u.GetSystemMetrics(0); sh=u.GetSystemMetrics(1)
 layouts={"left":(0,0,sw//2,sh),"right":(sw//2,0,sw//2,sh),"top":(0,0,sw,sh//2),"bottom":(0,sh//2,sw,sh//2)}
 if mode not in layouts:return "Use left, right, top or bottom."
 x,y,w,h=layouts[mode];u.ShowWindow(hwnd,9);u.SetWindowPos(hwnd,0,x,y,w,h,0x0040)
 return f"Arranged '{title}' {mode}."
TOOL={"name":"window_snap_layout","description":"Arrange a named Windows window into left, right, top or bottom half of the primary screen.","parameters":{"type":"OBJECT","properties":{"mode":{"type":"STRING"},"title":{"type":"STRING"}},"required":["mode","title"]},"handler":window_snap_layout}
