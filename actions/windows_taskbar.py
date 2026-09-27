"""Normal Windows taskbar shortcuts."""
import ctypes,platform,pyautogui
from core.permissions import permission_decision
from core import confirm
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_taskbar(parameters=None,**kwargs):
 if not kwargs.get("_permission_token"):
  p=dict(parameters or {});d,r=permission_decision("windows_taskbar",p)
  if d=="deny":return f"Permission denied: {r}"
  if d=="confirm":return confirm.request(key="windows_taskbar",title="Allow JARVIS: windows_taskbar?",detail=f"{r}. Waiting for your confirmation.",run=lambda:windows_taskbar(p,_permission_token=True))
 p=parameters or {};action=str(p.get("action","show")).lower()
 if action not in ("show","hide"):return "Action must be show or hide."
 u=ctypes.windll.user32;h=u.FindWindowW("Shell_TrayWnd",None)
 if not h:return "Taskbar window not found."
 u.ShowWindow(h,5 if action=="show" else 0);return f"Taskbar: {action}."
TOOL={"name":"windows_taskbar","description":"Show or hide the Windows taskbar window.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}}},"handler":windows_taskbar}