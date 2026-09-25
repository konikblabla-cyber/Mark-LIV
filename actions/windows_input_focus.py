"""Windows foreground input/focus diagnostics."""
import ctypes
import platform

def windows_input_focus(parameters=None, **kwargs):
    if platform.system() != "Windows":
        return "Windows-only action."
    try:
        u = ctypes.windll.user32
        hwnd = u.GetForegroundWindow()
        if not hwnd:
            return "No foreground window."
        pid = ctypes.c_ulong()
        if not u.GetWindowThreadProcessId(hwnd, ctypes.byref(pid)):
            return "Could not determine foreground process."
        return f"Foreground window HWND={hwnd}, PID={pid.value}."
    except (AttributeError, OSError) as exc:
        return f"Could not read input focus: {exc}"

TOOL={"name":"windows_input_focus","description":"Read-only Windows foreground window and owning PID for input focus diagnostics.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_input_focus}
