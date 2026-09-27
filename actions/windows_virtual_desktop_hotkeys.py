"""Normal Windows virtual-desktop shortcuts."""
import platform
from core.permissions import permission_decision
from core import confirm,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_virtual_desktop_hotkeys(parameters=None,**kwargs):
    if not kwargs.get("_permission_token"):
        p=dict(parameters or {})
        d,r=permission_decision("windows_virtual_desktop_hotkeys",p)
        if d=="deny": return f"Permission denied: {r}"
        if d=="confirm":
            return confirm.request(key="windows_virtual_desktop_hotkeys",title="Allow JARVIS: windows_virtual_desktop_hotkeys?",detail=f"{r}. Waiting for your confirmation.",run=lambda: windows_virtual_desktop_hotkeys(p,_permission_token=True))
    p=parameters or {}; action=str(p.get("action","overview")).lower()
    keys={"overview":["win","tab"],"new":["win","ctrl","d"],"close":["win","ctrl","f4"]}
    if action not in keys:return "Action must be overview, new, or close."
    pyautogui.hotkey(*keys[action])
    return f"Virtual desktop action: {action}."
TOOL={"name":"windows_virtual_desktop_hotkeys","description":"Use normal Windows shortcuts to open Task View, create a virtual desktop, or close the current virtual desktop.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}}},"handler":windows_virtual_desktop_hotkeys}
