"""Read-only Windows user-input idle time."""
import ctypes
import platform

class LASTINPUT(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

def windows_input_idle(parameters=None, **kwargs):
    if platform.system() != "Windows":
        return "Windows-only action."
    try:
        u = ctypes.windll.user32
        li = LASTINPUT(ctypes.sizeof(LASTINPUT))
        if not u.GetLastInputInfo(ctypes.byref(li)):
            return "Unable to read input idle time."
        now = ctypes.windll.kernel32.GetTickCount()
        ms = (now - li.dwTime) & 0xffffffff
        return f"User input idle: {ms / 1000:.1f}s."
    except (AttributeError, OSError) as exc:
        return f"Could not read input idle time: {exc}"

TOOL={"name":"windows_input_idle","description":"Read-only seconds since the last keyboard or mouse input on Windows.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_input_idle}
