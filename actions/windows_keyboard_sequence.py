"""Bounded Windows keyboard sequence action."""
import platform,time
from pyautogui import hotkey,press
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_keyboard_sequence(parameters=None,**kwargs):
 p=parameters or {}; seq=p.get("keys",[]); delay=max(0,min(float(p.get("delay",0.15)),2.0))
 if not isinstance(seq,list) or len(seq)>30:return "keys must be a list of at most 30 key names."
 for key in seq:
  k=str(key).strip().lower()
  if not k:continue
  press(k);time.sleep(delay)
 return f"Pressed {len(seq)} keys."
TOOL={"name":"windows_keyboard_sequence","description":"Execute a bounded sequence of normal keyboard key presses on Windows.","parameters":{"type":"OBJECT","properties":{"keys":{"type":"ARRAY","items":{"type":"STRING"}},"delay":{"type":"NUMBER"}},"required":["keys"]},"handler":windows_keyboard_sequence}
