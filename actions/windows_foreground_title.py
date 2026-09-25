"""Read-only Windows foreground window title."""
import ctypes
import platform

def windows_foreground_title(parameters=None, **kwargs):
    if platform.system() != "Windows":
        return "Windows-only action."
    try:
        u = ctypes.windll.user32
        hwnd = u.GetForegroundWindow()
        if not hwnd:
            return "No foreground window."
        n = u.GetWindowTextLengthW(hwnd)
        buf = ctypes.create_unicode_buffer(n + 1)
        u.GetWindowTextW(hwnd, buf, n + 1)
        return f"Foreground title: {buf.value or '<untitled>'}."
    except (AttributeError, OSError) as exc:
        return f"Could not read foreground window title: {exc}"

TOOL={"name":"windows_foreground_title","description":"Read-only title of the current Windows foreground window.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_foreground_title}
