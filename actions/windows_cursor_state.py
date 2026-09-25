"""Read-only Windows cursor state."""
import ctypes, platform
from ctypes import wintypes
if platform.system() != "Windows":
    raise RuntimeError("Windows-only.")
class _CURSORINFO(ctypes.Structure):
    _fields_=[("cbSize",ctypes.c_uint),("flags",ctypes.c_uint),("hCursor",ctypes.c_void_p),("ptScreenPos",wintypes.POINT)]
def windows_cursor_state(parameters=None,**kwargs):
    u=ctypes.windll.user32; pos=wintypes.POINT()
    u.GetCursorPos(ctypes.byref(pos))
    ci=_CURSORINFO(ctypes.sizeof(_CURSORINFO)); u.GetCursorInfo(ctypes.byref(ci))
    return f"Cursor: x={pos.x}, y={pos.y}; visible={bool(ci.flags & 1)}."
TOOL={"name":"windows_cursor_state","description":"Read-only Windows cursor position and visibility state.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_cursor_state}
