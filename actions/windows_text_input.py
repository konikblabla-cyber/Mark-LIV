"""Windows text entry action."""
import platform,time,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_text_input(parameters=None,**kwargs):
 p=parameters or {}; text=str(p.get("text",""))
 if not text:return "Text is required."
 if len(text)>4000:return "Text is limited to 4000 characters."
 pyautogui.write(text,interval=.002)
 return f"Typed {len(text)} characters into the focused Windows control."
TOOL={"name":"windows_text_input","description":"Type bounded text into the currently focused Windows control.","parameters":{"type":"OBJECT","properties":{"text":{"type":"STRING"}},"required":["text"]},"handler":windows_text_input}
