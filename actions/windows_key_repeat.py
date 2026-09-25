"""Bounded Windows key repetition."""
import platform,time,pyautogui

def windows_key_repeat(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {};key=str(p.get("key","")).strip()
 try:count=max(1,min(int(p.get("count",1)),30));interval=max(.03,min(float(p.get("interval",.1)),2))
 except (TypeError,ValueError):return "Invalid count or interval."
 if not key:return "Missing key."
 try:
  for _ in range(count):pyautogui.press(key);time.sleep(interval)
 except (pyautogui.FailSafeException,OSError) as e:return f"Key repetition failed: {e}"
 return f"Pressed {key} {count} time(s)."
TOOL={"name":"windows_key_repeat","description":"Press a normal Windows keyboard key repeatedly with bounded count and interval.","parameters":{"type":"OBJECT","properties":{"key":{"type":"STRING"},"count":{"type":"INTEGER"},"interval":{"type":"NUMBER"}},"required":["key"]},"handler":windows_key_repeat}