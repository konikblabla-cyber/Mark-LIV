"""Check whether a Windows UI Automation control exists."""
import platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_element_exists(parameters=None,**kwargs):
 p=parameters or {}; title=str(p.get("title") or "").strip()
 if not title:return "Missing control title."
 try:
  from pywinauto import Desktop
  count=0
  for w in Desktop(backend="uia").windows():
   try: count+=sum(1 for c in w.descendants() if str(c.window_text() or "")==title)
   except Exception: pass
  return f"UI control '{title}' exists: {count>0} (matches={count})."
 except Exception as e:return f"UIA lookup failed: {e}"
TOOL={"name":"windows_ui_element_exists","description":"Check whether a visible Windows UI Automation control with exact title exists.","parameters":{"type":"OBJECT","properties":{"title":{"type":"STRING"}},"required":["title"]},"handler":windows_ui_element_exists}
