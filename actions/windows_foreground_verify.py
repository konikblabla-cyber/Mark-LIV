"""Verify the Windows foreground application."""
import ctypes
import platform

def windows_foreground_verify(parameters=None, **kwargs):
    if platform.system() != "Windows":
        return "Windows-only action."
    p = parameters or {}
    expected = str(p.get("contains") or p.get("title") or "").strip().lower()
    try:
        u = ctypes.windll.user32
        hwnd = u.GetForegroundWindow()
        if not hwnd:
            return "No foreground window."
        n = u.GetWindowTextLengthW(hwnd)
        b = ctypes.create_unicode_buffer(n + 1)
        u.GetWindowTextW(hwnd, b, n + 1)
        title = b.value
        if expected and expected not in title.lower():
            return f"Foreground verification failed: '{title}'."
        return f"Foreground verified: '{title}'."
    except (AttributeError, OSError) as exc:
        return f"Could not verify foreground window: {exc}"

TOOL={"name":"windows_foreground_verify","description":"Verify expected text in the current Windows foreground window title.","parameters":{"type":"OBJECT","properties":{"contains":{"type":"STRING"},"title":{"type":"STRING"}}},"handler":windows_foreground_verify}
