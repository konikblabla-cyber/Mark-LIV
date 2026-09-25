"""Windows workflow keyboard primitive with bounded validation."""
import platform,time,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_workflow_key(parameters=None,**kwargs):
 p=parameters or {}; key=str(p.get("key") or "").strip().lower(); delay=max(0,min(float(p.get("delay",0.15)),3))
 if not key:return "Missing key."
 pyautogui.press(key);time.sleep(delay)
 return f"Pressed key: {key}."
TOOL={"name":"windows_workflow_key","description":"Press one normal Windows keyboard key as a workflow step.","parameters":{"type":"OBJECT","properties":{"key":{"type":"STRING"},"delay":{"type":"NUMBER"}},"required":["key"]},"handler":windows_workflow_key}
