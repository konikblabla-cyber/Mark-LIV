"""Useful normal Windows hotkeys."""
import platform
from core.permissions import permission_decision
from core import confirm
import pyautogui

HOTKEYS={"task_view":("win","tab"),"search":("win","s"),"settings":("win","i"),"run":("win","r"),"file_explorer":("win","e")}

def windows_hotkey_action(parameters=None, **kwargs):

    if not kwargs.get("_permission_token"):
        p = dict(parameters or {})
        decision, reason = permission_decision("windows_hotkey_action", p)
        if decision == "deny":
            return f"Permission denied: {reason}"
        if decision == "confirm":
            return confirm.request(key="windows_hotkey_action", title="Allow JARVIS: windows_hotkey_action?", detail=f"{reason}. Waiting for your confirmation.", run=lambda: windows_hotkey_action(p, _permission_token=True))
    if platform.system() != "Windows":
        return "Windows-only action."
    p = parameters or {}
    action = str(p.get("action", "")).strip().lower()
    if action not in HOTKEYS:
        return "Unknown action. Use task_view, search, settings, run, or file_explorer."
    try:
        pyautogui.hotkey(*HOTKEYS[action])
        return f"Hotkey action executed: {action}."
    except Exception as exc:
        return f"Hotkey action failed: {exc}"

TOOL={"name":"windows_hotkey_action","description":"Open common Windows interfaces using their normal keyboard shortcuts.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}}},"handler":windows_hotkey_action}
