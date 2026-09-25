"""Windows foreground input/focus diagnostics."""
import ctypes, platform
if platform.system() != "Windows":
    raise RuntimeError("Windows-only.")
def windows_input_focus(parameters=None, **kwargs):
    u=ctypes.windll.user32
    hwnd=u.GetForegroundWindow()
    pid=ctypes.c_ulong()
    u.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return f"Foreground window HWND={hwnd}, PID={pid.value}."
TOOL={"name":"windows_input_focus","description":"Read-only Windows foreground window and owning PID for input focus diagnostics.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_input_focus}
