"""Read text from a uniquely matched visible Windows UI control."""
import platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_element_text(parameters=None,**kwargs):
 p=parameters or {}; title=str(p.get("title") or "").strip()
 if not title:return "Missing control title."
 try:
  from pywinauto import Desktop
  wins=Desktop(backend="uia").windows()
  matches=[]
  for w in wins:
   try:
    for c in w.descendants():
     name=str(c.window_text() or "")
     if name==title: matches.append(name)
   except Exception: pass
  if len(matches)==1:return matches[0]
  return f"Found {len(matches)} matching controls for '{title}'."
 except Exception as e:return f"UIA read failed: {e}"
TOOL={"name":"windows_ui_element_text","description":"Read text from a uniquely matched visible Windows UI Automation control by exact title.","parameters":{"type":"OBJECT","properties":{"title":{"type":"STRING"}},"required":["title"]},"handler":windows_ui_element_text}
