"""Inspect a visible Windows UI element by text using UI Automation."""
import platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_element(parameters=None,**kwargs):
 p=parameters or {}; text=str(p.get("text") or "").strip()
 if not text:return "Missing UI element text."
 try:
  from pywinauto import Desktop
  wins=Desktop(backend="uia").windows(visible_only=True)
  hits=[]
  for w in wins:
   try:
    for c in w.descendants():
     name=(c.window_text() or "").strip()
     if text.lower() in name.lower(): hits.append(f"{name} | control={c.element_info.control_type} | window={w.window_text()}")
   except Exception: continue
  return "\n".join(hits[:50]) if hits else f"No visible UI element matched: {text}"
 except Exception as e:return f"UI Automation unavailable: {e}"
TOOL={"name":"windows_ui_element","description":"Find visible Windows UI Automation controls by displayed text without clicking or changing anything.","parameters":{"type":"OBJECT","properties":{"text":{"type":"STRING"}},"required":["text"]},"handler":windows_ui_element}
