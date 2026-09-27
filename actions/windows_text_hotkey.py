"""Type text followed by an optional normal Windows hotkey."""
import platform
from core.permissions import permission_decision
from core import confirm
import pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_text_hotkey(parameters=None,**kwargs):
    if not kwargs.get("_permission_token"):
        p=dict(parameters or {})
        d,r=permission_decision("windows_text_hotkey",p)
        if d=="deny": return f"Permission denied: {r}"
        if d=="confirm":
            return confirm.request(key="windows_text_hotkey",title="Allow JARVIS: windows_text_hotkey?",detail=f"{r}. Waiting for your confirmation.",run=lambda: windows_text_hotkey(p,_permission_token=True))
    p=parameters or {};text=str(p.get("text",""));keys=p.get("hotkey",[])
    if len(text)>4000:return "Text too long (max 4000 characters)."
    if keys and (not isinstance(keys,list) or len(keys)>5):return "hotkey must contain up to 5 keys."
    if text:pyautogui.write(text,interval=max(0,min(float(p.get("interval",.01)),.2)))
    if keys:pyautogui.hotkey(*[str(k) for k in keys])
    return "Text typed and optional hotkey sent."
TOOL={"name":"windows_text_hotkey","description":"Type bounded text into the focused Windows control and optionally send a normal hotkey.","parameters":{"type":"OBJECT","properties":{"text":{"type":"STRING"},"hotkey":{"type":"ARRAY"},"interval":{"type":"NUMBER"}}},"handler":windows_text_hotkey}
