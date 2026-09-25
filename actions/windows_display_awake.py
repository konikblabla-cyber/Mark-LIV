"""Keep Windows display/system awake temporarily."""
import ctypes,platform
ES_CONTINUOUS=0x80000000;ES_DISPLAY_REQUIRED=0x2;ES_SYSTEM_REQUIRED=0x1
def windows_display_awake(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; enable=bool(p.get("enable",True))
 flags=ES_CONTINUOUS|ES_DISPLAY_REQUIRED|ES_SYSTEM_REQUIRED if enable else ES_CONTINUOUS
 ctypes.windll.kernel32.SetThreadExecutionState(flags)
 return "Windows display/system sleep prevention enabled." if enable else "Windows sleep prevention released."
TOOL={"name":"windows_display_awake","description":"Temporarily keep the Windows display/system awake or release that requirement.","parameters":{"type":"OBJECT","properties":{"enable":{"type":"BOOLEAN"}}},"handler":windows_display_awake}
