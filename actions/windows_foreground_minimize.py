"""Minimize the current foreground Windows window."""
import ctypes,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_foreground_minimize(parameters=None,**kwargs):
 h=ctypes.windll.user32.GetForegroundWindow()
 if not h:return "No foreground window."
 ctypes.windll.user32.ShowWindow(h,6);return "Foreground window minimized."
TOOL={"name":"windows_foreground_minimize","description":"Minimize the current foreground Windows window.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_foreground_minimize}
