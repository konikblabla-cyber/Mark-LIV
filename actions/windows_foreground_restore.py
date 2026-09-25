"""Restore the current foreground Windows window."""
import ctypes,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_foreground_restore(parameters=None,**kwargs):
 h=ctypes.windll.user32.GetForegroundWindow()
 if not h:return "No foreground window."
 ctypes.windll.user32.ShowWindow(h,9);return "Foreground window restored."
TOOL={"name":"windows_foreground_restore","description":"Restore the current foreground Windows window from minimized state.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_foreground_restore}
