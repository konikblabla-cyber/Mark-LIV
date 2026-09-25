"""Type text followed by an optional normal Windows hotkey."""
import platform,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_text_hotkey(parameters=None,**kwargs):
 p=parameters or {};text=str(p.get("text",""));keys=p.get("hotkey",[])
 if len(text)>4000:return "Text too long (max 4000 characters)."
 if keys and (not isinstance(keys,list) or len(keys)>5):return "hotkey must contain up to 5 keys."
 if text:pyautogui.write(text,interval=max(0,min(float(p.get("interval",.01)),.2)))
 if keys:pyautogui.hotkey(*[str(k) for k in keys])
 return "Text typed and optional hotkey sent."
TOOL={"name":"windows_text_hotkey","description":"Type bounded text into the focused Windows control and optionally send a normal hotkey.","parameters":{"type":"OBJECT","properties":{"text":{"type":"STRING"},"hotkey":{"type":"ARRAY"},"interval":{"type":"NUMBER"}}},"handler":windows_text_hotkey}
