"""Read-only Windows cursor state."""
import platform,ctypes
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_cursor_state(parameters=None,**kwargs):
 u=ctypes.windll.user32; pos=ctypes.wintypes.POINT();u.GetCursorPos(ctypes.byref(pos))
 return f"Cursor: x={pos.x}, y={pos.y}; visible={bool(u.GetCursorInfo(ctypes.byref(type('CI',(ctypes.Structure,),{'_fields_':[('cbSize',ctypes.c_uint),('flags',ctypes.c_uint),('hCursor',ctypes.c_void_p),('ptScreenPos',ctypes.wintypes.POINT)]})(ctypes.sizeof(ctypes.c_uint)*4)) ))}."
TOOL={"name":"windows_cursor_state","description":"Read-only Windows cursor position and state.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_cursor_state}
