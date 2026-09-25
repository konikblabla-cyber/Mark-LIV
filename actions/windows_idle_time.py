"""Read-only Windows user idle time."""
import ctypes
import platform

class LI(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

def windows_idle_time(parameters=None, **kwargs):
    if platform.system() != "Windows":
        return "Windows-only action."
    try:
        u = ctypes.windll.user32
        i = LI()
        i.cbSize = ctypes.sizeof(LI)
        if not u.GetLastInputInfo(ctypes.byref(i)):
            return "Unable to read idle time."
        tick = ctypes.windll.kernel32.GetTickCount()
        sec = max(0, (tick - i.dwTime) & 0xffffffff) / 1000
        return f"User idle time: {sec:.1f}s."
    except (AttributeError, OSError) as exc:
        return f"Could not read idle time: {exc}"

TOOL={"name":"windows_idle_time","description":"Read-only seconds since last keyboard or mouse input on Windows.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_idle_time}
