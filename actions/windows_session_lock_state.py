"""Read-only Windows interactive-session indicator."""
import ctypes,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_session_lock_state(parameters=None,**kwargs):
 u=ctypes.windll.user32; hwnd=u.GetForegroundWindow()
 return f"Foreground window available: {bool(hwnd)}; interactive desktop handle: {bool(u.GetDesktopWindow())}."
TOOL={"name":"windows_session_lock_state","description":"Read-only indicator of interactive Windows session availability.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_session_lock_state}
