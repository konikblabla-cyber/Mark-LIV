"""Minimize the current foreground Windows window."""
import ctypes
import platform

def windows_foreground_minimize(parameters=None, **kwargs):
    if platform.system() != "Windows":
        return "Windows-only action."
    try:
        h = ctypes.windll.user32.GetForegroundWindow()
        if not h:
            return "No foreground window."
        ctypes.windll.user32.ShowWindow(h, 6)
        return "Foreground window minimized."
    except (AttributeError, OSError) as exc:
        return f"Could not minimize foreground window: {exc}"

TOOL={"name":"windows_foreground_minimize","description":"Minimize the current foreground Windows window.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_foreground_minimize}
