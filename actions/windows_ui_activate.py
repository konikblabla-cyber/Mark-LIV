"""Activate a uniquely matched Windows UI Automation window."""
import platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_activate(parameters=None,**kwargs):
 p=parameters or {}; title=str(p.get("title") or "").strip()
 if not title:return "Missing window title."
 try:
  from pywinauto import Desktop
  matches=[w for w in Desktop(backend="uia").windows(visible_only=True) if title.lower() in w.window_text().lower()]
  if len(matches)!=1:return f"Expected exactly one matching window, found {len(matches)}."
  matches[0].set_focus(); return f"Activated window: {matches[0].window_text()}"
 except Exception as e:return f"Window activation failed: {e}"
TOOL={"name":"windows_ui_activate","description":"Focus one uniquely matched visible Windows window using UI Automation.","parameters":{"type":"OBJECT","properties":{"title":{"type":"STRING"}},"required":["title"]},"handler":windows_ui_activate}
