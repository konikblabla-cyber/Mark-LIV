"""Recover common Windows UI input focus without bypassing security."""
import ctypes
import platform
import pyautogui
import time

def windows_input_recovery(parameters=None, **kwargs):
    if platform.system() != "Windows":
        return "Windows-only action."
    p = parameters or {}
    target = str(p.get("title_contains") or "").strip()
    try:
        if target:
            u = ctypes.windll.user32
            pyautogui.hotkey("alt", "tab")
            time.sleep(0.25)
            hwnd = u.GetForegroundWindow()
            n = u.GetWindowTextLengthW(hwnd)
            b = ctypes.create_unicode_buffer(n + 1)
            u.GetWindowTextW(hwnd, b, n + 1)
            return f"Focus recovery attempted; active window='{b.value}'."
        pyautogui.hotkey("esc")
        return "Focus recovery: sent Escape to the active window."
    except (AttributeError, OSError, pyautogui.FailSafeException) as exc:
        return f"Focus recovery failed: {exc}"

TOOL={"name":"windows_input_recovery","description":"Recover from common UI focus mistakes using normal Windows input; never bypasses UAC or security dialogs.","parameters":{"type":"OBJECT","properties":{"title_contains":{"type":"STRING"}}},"handler":windows_input_recovery}
