"""Click a uniquely matched Windows UI Automation control."""
import platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_element_click(parameters=None,**kwargs):
 p=parameters or {}; title=str(p.get("title") or "").strip()
 if not title:return "Missing control title."
 try:
  from pywinauto import Desktop
  matches=[]
  for w in Desktop(backend="uia").windows():
   try:
    for c in w.descendants():
     if str(c.window_text() or "")==title: matches.append(c)
   except Exception: pass
  if len(matches)!=1:return f"Expected one matching control, found {len(matches)}."
  matches[0].click_input()
  return f"Clicked UI control '{title}'."
 except Exception as e:return f"UIA click failed: {e}"
TOOL={"name":"windows_ui_element_click","description":"Click a uniquely matched visible Windows UI Automation control by exact title.","parameters":{"type":"OBJECT","properties":{"title":{"type":"STRING"}},"required":["title"]},"handler":windows_ui_element_click}
