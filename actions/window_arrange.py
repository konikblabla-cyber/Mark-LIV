"""Windows-only simple window arrangement."""
import platform,ctypes
from ctypes import wintypes
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
u=ctypes.windll.user32
def window_arrange(parameters=None,**kwargs):
 p=parameters or {}; a=str(p.get("action","tile")).lower().strip()
 if a not in ("tile","cascade","minimize_all"):return "Use tile, cascade or minimize_all."
 if a=="minimize_all":
  u.ShowWindow(u.GetDesktopWindow(),6); return "Minimize-all requested."
 flags=0x0002 if a=="tile" else 0x0010
 u.TileWindows(0,flags,0,0,None) if a=="tile" else u.CascadeWindows(0,0,0,0,None)
 return f"Windows {a} requested."
TOOL={"name":"window_arrange","description":"Windows-only window layout helper: tile or cascade top-level windows, or request minimize-all. No application data is changed.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}},"required":["action"]},"handler":window_arrange}
