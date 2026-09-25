"""Read-only Windows user-input idle time."""
import ctypes,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
class LASTINPUT(ctypes.Structure):
 _fields_=[("cbSize",ctypes.c_uint),("dwTime",ctypes.c_uint)]
def windows_input_idle(parameters=None,**kwargs):
 u=ctypes.windll.user32; li=LASTINPUT(ctypes.sizeof(LASTINPUT));u.GetLastInputInfo(ctypes.byref(li))
 now=ctypes.windll.kernel32.GetTickCount();ms=(now-li.dwTime)&0xffffffff
 return f"User input idle: {ms/1000:.1f}s."
TOOL={"name":"windows_input_idle","description":"Read-only seconds since the last keyboard or mouse input on Windows.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_input_idle}
