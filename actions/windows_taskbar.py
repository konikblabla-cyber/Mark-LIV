"""Normal Windows taskbar shortcuts."""
import ctypes,platform,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_taskbar(parameters=None,**kwargs):
 p=parameters or {};action=str(p.get("action","show")).lower()
 if action not in ("show","hide"):return "Action must be show or hide."
 u=ctypes.windll.user32;h=u.FindWindowW("Shell_TrayWnd",None)
 if not h:return "Taskbar window not found."
 u.ShowWindow(h,5 if action=="show" else 0);return f"Taskbar: {action}."
TOOL={"name":"windows_taskbar","description":"Show or hide the Windows taskbar window.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}}},"handler":windows_taskbar}
