"""Read-only current Windows mouse position."""
import platform,ctypes
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
class PT(ctypes.Structure):_fields_=[("x",ctypes.c_long),("y",ctypes.c_long)]
def windows_mouse_position(parameters=None,**kwargs):
 p=PT()
 if not ctypes.windll.user32.GetCursorPos(ctypes.byref(p)):return "Could not read mouse position."
 return f"Mouse position: x={p.x}, y={p.y}"
TOOL={"name":"windows_mouse_position","description":"Read-only current Windows mouse cursor coordinates.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_mouse_position}
