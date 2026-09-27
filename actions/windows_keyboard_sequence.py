"""Bounded Windows keyboard sequence action."""
import platform,time
from core.permissions import permission_decision
from core import confirm
from pyautogui import hotkey,press
def windows_keyboard_sequence(parameters=None,**kwargs):

             if not kwargs.get("_permission_token"):
                 p = dict(parameters or {})
                 decision, reason = permission_decision("windows_keyboard_sequence", p)
                 if decision == "deny":
                     return f"Permission denied: {reason}"
                 if decision == "confirm":
                     return confirm.request(key="windows_keyboard_sequence", title="Allow JARVIS: windows_keyboard_sequence?", detail=f"{reason}. Waiting for your confirmation.", run=lambda: windows_keyboard_sequence(p, _permission_token=True))
    if platform.system()!="Windows": return "Windows-only action."
    p=parameters or {}; seq=p.get("keys",[]); delay=max(0,min(float(p.get("delay",0.15)),2.0))
    if not isinstance(seq,list) or len(seq)>30:return "keys must be a list of at most 30 key names."
    for key in seq:
        k=str(key).strip().lower()
        if not k:continue
        press(k);time.sleep(delay)
    return f"Pressed {len(seq)} keys."
TOOL={"name":"windows_keyboard_sequence","description":"Execute a bounded sequence of normal keyboard key presses on Windows.","parameters":{"type":"OBJECT","properties":{"keys":{"type":"ARRAY","items":{"type":"STRING"}},"delay":{"type":"NUMBER"}},"required":["keys"]},"handler":windows_keyboard_sequence}
