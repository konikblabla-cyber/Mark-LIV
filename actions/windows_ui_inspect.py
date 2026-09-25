"""Inspect visible Windows UI controls using UI Automation."""
import platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_inspect(parameters=None,**kwargs):
 p=parameters or {}
 try:
  from pywinauto import Desktop
  title=str(p.get("title") or "").strip()
  wins=Desktop(backend="uia").windows(visible_only=True)
  out=[]
  for w in wins[:30]:
   if title and title.lower() not in w.window_text().lower(): continue
   out.append(f"WINDOW: {w.window_text() or '<untitled>'}")
   try:
    for c in w.descendants(depth=2)[:40]:
     name=c.window_text()
     if name: out.append(f"  {c.element_info.control_type}: {name}")
   except Exception: pass
  return "\n".join(out)[:7000] or "No matching visible UI elements."
 except Exception as e: return f"UI Automation unavailable: {e}"
TOOL={"name":"windows_ui_inspect","description":"Inspect visible Windows UI Automation controls and labels, optionally filtered by window title.","parameters":{"type":"OBJECT","properties":{"title":{"type":"STRING"}}},"handler":windows_ui_inspect}
