"""Read-only Windows idle-time inspection."""
import platform,ctypes
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
class LI(ctypes.Structure):_fields_=[("cbSize",ctypes.c_uint),("dwTime",ctypes.c_uint)]
def windows_system_idle(parameters=None,**kwargs):
 i=LI();i.cbSize=ctypes.sizeof(LI)
 if not ctypes.windll.user32.GetLastInputInfo(ctypes.byref(i)):return "Could not read idle time."
 now=ctypes.windll.kernel32.GetTickCount(); sec=max(0,(now-i.dwTime)//1000)
 return f"Windows user idle time: {sec} seconds."
TOOL={"name":"windows_system_idle","description":"Read-only Windows user idle time since last keyboard or mouse input.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_system_idle}
