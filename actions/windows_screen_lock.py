"""Lock the Windows workstation."""
import platform,ctypes
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_screen_lock(parameters=None,**kwargs):
    ctypes.windll.user32.LockWorkStation()
    return "Windows workstation lock requested."
TOOL={"name":"windows_screen_lock","description":"Lock the Windows workstation using the normal Windows lock API.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_screen_lock}
