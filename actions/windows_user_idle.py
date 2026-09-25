"""Read-only Windows user idle duration."""
import ctypes,platform,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
class LASTINPUT(ctypes.Structure): _fields_=[("cbSize",ctypes.c_uint),("dwTime",ctypes.c_uint)]
def windows_user_idle(parameters=None,**kwargs):
 x=LASTINPUT(ctypes.sizeof(LASTINPUT));ctypes.windll.user32.GetLastInputInfo(ctypes.byref(x))
 now=ctypes.windll.kernel32.GetTickCount();secs=max(0,(now-x.dwTime)&0xffffffff)/1000
 return f"User idle time: {secs:.1f}s."
TOOL={"name":"windows_user_idle","description":"Read-only time since the last keyboard or mouse input on Windows.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_user_idle}
