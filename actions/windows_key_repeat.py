"""Bounded Windows key repetition."""
import platform,time,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_key_repeat(parameters=None,**kwargs):
 p=parameters or {};key=str(p.get("key","")).strip();count=max(1,min(int(p.get("count",1)),30));interval=max(.03,min(float(p.get("interval",.1)),2))
 if not key:return "Missing key."
 for _ in range(count):pyautogui.press(key);time.sleep(interval)
 return f"Pressed {key} {count} time(s)."
TOOL={"name":"windows_key_repeat","description":"Press a normal Windows keyboard key repeatedly with bounded count and interval.","parameters":{"type":"OBJECT","properties":{"key":{"type":"STRING"},"count":{"type":"INTEGER"},"interval":{"type":"NUMBER"}},"required":["key"]},"handler":windows_key_repeat}
