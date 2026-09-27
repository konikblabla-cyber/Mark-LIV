"""Lock the Windows workstation."""
import platform,ctypes
from core.permissions import permission_decision
from core import confirm
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_screen_lock(parameters=None,**kwargs):
    if not kwargs.get("_permission_token"):
        p=dict(parameters or {})
        decision,reason=permission_decision("windows_screen_lock",p)
        if decision=="deny": return f"Permission denied: {reason}"
        if decision=="confirm":
            return confirm.request(key="windows_screen_lock",title="Allow JARVIS: windows_screen_lock?",detail=f"{reason}. Waiting for your confirmation.",run=lambda: windows_screen_lock(p,_permission_token=True))
    ctypes.windll.user32.LockWorkStation()
    return "Windows workstation lock requested."
TOOL={"name":"windows_screen_lock","description":"Lock the Windows workstation using the normal Windows lock API.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_screen_lock}