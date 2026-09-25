"""Read-only Windows cursor visibility."""
import ctypes,platform
class CURSORINFO(ctypes.Structure):
 _fields_=[("cbSize",ctypes.c_uint),("flags",ctypes.c_uint),("hCursor",ctypes.c_void_p),("ptScreenPos",ctypes.wintypes.POINT)]
def windows_cursor_visible(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 u=ctypes.windll.user32;ci=CURSORINFO();ci.cbSize=ctypes.sizeof(CURSORINFO);u.GetCursorInfo(ctypes.byref(ci))
 return f"Cursor visible={bool(ci.flags & 1)}; x={ci.ptScreenPos.x}; y={ci.ptScreenPos.y}."
TOOL={"name":"windows_cursor_visible","description":"Read-only Windows cursor visibility and screen position.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_cursor_visible}
