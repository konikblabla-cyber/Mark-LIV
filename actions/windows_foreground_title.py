"""Read-only Windows foreground window title."""
import ctypes, platform
if platform.system() != "Windows":
    raise RuntimeError("Windows-only.")
def windows_foreground_title(parameters=None, **kwargs):
    u=ctypes.windll.user32; hwnd=u.GetForegroundWindow()
    n=u.GetWindowTextLengthW(hwnd); buf=ctypes.create_unicode_buffer(n+1); u.GetWindowTextW(hwnd,buf,n+1)
    return f"Foreground title: {buf.value or '<untitled>'}."
TOOL={"name":"windows_foreground_title","description":"Read-only title of the current Windows foreground window.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_foreground_title}
