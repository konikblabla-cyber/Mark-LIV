"""Windows workflow text-entry primitive."""
import platform,time,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_workflow_type(parameters=None,**kwargs):
 p=parameters or {}; text=str(p.get("text") or "")
 if len(text)>2000:return "Text too long; maximum is 2000 characters."
 pyautogui.write(text,interval=max(0,min(float(p.get("interval",0.01)),0.2)));time.sleep(max(0,min(float(p.get("delay",0.15)),3)))
 return f"Typed {len(text)} characters."
TOOL={"name":"windows_workflow_type","description":"Type bounded text into the currently focused Windows control as one workflow step.","parameters":{"type":"OBJECT","properties":{"text":{"type":"STRING"},"interval":{"type":"NUMBER"},"delay":{"type":"NUMBER"}},"required":["text"]},"handler":windows_workflow_type}
