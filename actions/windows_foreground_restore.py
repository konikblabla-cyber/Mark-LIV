"""Restore the current foreground Windows window."""
import ctypes
import platform

def windows_foreground_restore(parameters=None, **kwargs):
    if platform.system() != "Windows":
        return "Windows-only action."
    try:
        h = ctypes.windll.user32.GetForegroundWindow()
        if not h:
            return "No foreground window."
        ctypes.windll.user32.ShowWindow(h, 9)
        return "Foreground window restored."
    except (AttributeError, OSError) as exc:
        return f"Could not restore foreground window: {exc}"

TOOL={"name":"windows_foreground_restore","description":"Restore the current foreground Windows window from minimized state.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_foreground_restore}
