"""Windows text entry action."""
import platform
from core.permissions import permission_decision
from core import confirm,time,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_text_input(parameters=None,**kwargs):
                      if not kwargs.get("_permission_token"):
                          p=dict(parameters or {})
                          d,r=permission_decision("windows_text_input",p)
                          if d=="deny": return f"Permission denied: {r}"
                          if d=="confirm":
                              return confirm.request(key="windows_text_input",title="Allow JARVIS: windows_text_input?",detail=f"{r}. Waiting for your confirmation.",run=lambda: windows_text_input(p,_permission_token=True))
             p=parameters or {}; text=str(p.get("text",""))
             if not text:return "Text is required."
             if len(text)>4000:return "Text is limited to 4000 characters."
             pyautogui.write(text,interval=.002)
             return f"Typed {len(text)} characters into the focused Windows control."
TOOL={"name":"windows_text_input","description":"Type bounded text into the currently focused Windows control.","parameters":{"type":"OBJECT","properties":{"text":{"type":"STRING"}},"required":["text"]},"handler":windows_text_input}
