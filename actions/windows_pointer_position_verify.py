"""Verify Windows cursor position."""
import platform,ctypes
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_pointer_position_verify(parameters=None,**kwargs):
 p=parameters or {}
 try:x=int(p["x"]);y=int(p["y"]);t=max(0,min(int(p.get("tolerance",2)),100))
 except (KeyError,TypeError,ValueError):return "Missing valid x and y."
 pos=ctypes.wintypes.POINT();ctypes.windll.user32.GetCursorPos(ctypes.byref(pos))
 return f"Cursor=({pos.x},{pos.y}); target=({x},{y}); within_tolerance={abs(pos.x-x)<=t and abs(pos.y-y)<=t}."
TOOL={"name":"windows_pointer_position_verify","description":"Read-only verification that the Windows cursor reached a target point.","parameters":{"type":"OBJECT","properties":{"x":{"type":"INTEGER"},"y":{"type":"INTEGER"},"tolerance":{"type":"INTEGER"}},"required":["x","y"]},"handler":windows_pointer_position_verify}
