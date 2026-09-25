"""Control the foreground Windows window state."""
import ctypes,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
SW_MINIMIZE=6;SW_MAXIMIZE=3;SW_RESTORE=9
def windows_window_controls(parameters=None,**kwargs):
 p=parameters or {}; action=str(p.get("action","restore")).lower();u=ctypes.windll.user32;h=u.GetForegroundWindow()
 if not h:return "No foreground window."
 modes={"minimize":SW_MINIMIZE,"maximize":SW_MAXIMIZE,"restore":SW_RESTORE}
 if action not in modes:return "Action must be minimize, maximize, or restore."
 u.ShowWindow(h,modes[action]);return f"Foreground window: {action}."
TOOL={"name":"windows_window_controls","description":"Minimize, maximize, or restore the current foreground Windows window.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}}},"handler":windows_window_controls}
