"""Maximize the foreground Windows window."""
import ctypes,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_window_maximize(parameters=None,**kwargs):
 u=ctypes.windll.user32;h=u.GetForegroundWindow()
 if not h:return "No foreground window."
 u.ShowWindow(h,3);return "Foreground window maximized."
TOOL={"name":"windows_window_maximize","description":"Maximize the current foreground Windows window.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_window_maximize}
