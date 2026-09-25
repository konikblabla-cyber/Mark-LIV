"""Find accessible controls in the foreground Windows window."""
import platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_control_find(parameters=None,**kwargs):
 p=parameters or {}; needle=str(p.get("text") or "").strip().lower()
 if not needle:return "Missing text."
 try:
  from pywinauto import Desktop
  win=Desktop(backend="uia").get_active(); out=[]
  for c in win.descendants():
   try:
    text=c.window_text()
    if needle in text.lower(): out.append(f"{c.element_info.control_type}: {text[:120]}")
   except Exception: pass
  return "\n".join(out[:50]) if out else f"No accessible control matched: {needle}"
 except Exception as e:return f"Control search failed: {e}"
TOOL={"name":"windows_ui_control_find","description":"Read-only find accessible controls by visible text in the active Windows window.","parameters":{"type":"OBJECT","properties":{"text":{"type":"STRING"}},"required":["text"]},"handler":windows_ui_control_find}
