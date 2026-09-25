"""Read-only foreground Windows process details."""
import ctypes
import platform
import psutil

def windows_foreground_process(parameters=None, **kwargs):
    if platform.system() != "Windows":
        return "Windows-only action."
    try:
        u = ctypes.windll.user32
        hwnd = u.GetForegroundWindow()
        if not hwnd:
            return "No foreground window."
        pid = ctypes.c_ulong()
        if not u.GetWindowThreadProcessId(hwnd, ctypes.byref(pid)) or not pid.value:
            return "Could not determine foreground process."
        try:
            p = psutil.Process(pid.value)
            return f"Foreground PID={pid.value}; process={p.name()}; exe={p.exe()}"
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return f"Foreground PID={pid.value}; process details unavailable."
    except (AttributeError, OSError) as exc:
        return f"Could not read foreground process: {exc}"

TOOL={"name":"windows_foreground_process","description":"Read-only process name and executable path owning the foreground Windows window.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_foreground_process}
