"""Read-only Windows input idle duration."""
import ctypes,platform,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
class LASTINPUT(ctypes.Structure): _fields_=[("cbSize",ctypes.c_uint),("dwTime",ctypes.c_uint)]
def windows_ui_idle(parameters=None,**kwargs):
 u=ctypes.windll.user32; x=LASTINPUT(ctypes.sizeof(LASTINPUT));u.GetLastInputInfo(ctypes.byref(x))
 now=ctypes.windll.kernel32.GetTickCount(); ms=(now-x.dwTime)&0xffffffff
 return f"User input idle: {ms/1000:.1f}s."
TOOL={"name":"windows_ui_idle","description":"Read-only time since the last keyboard or mouse input on Windows.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_ui_idle}
