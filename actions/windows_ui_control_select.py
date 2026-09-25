"""Select an item in a uniquely identified Windows UI Automation control."""
import platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_control_select(parameters=None,**kwargs):
    p=parameters or {}; title=str(p.get("title") or "").strip(); item=str(p.get("item") or "").strip()
    if not title or not item:return "Missing control title or item."
    try:
        from pywinauto import Desktop
        win=Desktop(backend="uia"); c=win.get_active().child_window(title=title)
        if not c.exists(timeout=2): return f"Control not found: {title}"
        c.select(item); return f"Selected '{item}' in {title}."
    except Exception as e:return f"UI selection failed: {e}"
TOOL={"name":"windows_ui_control_select","description":"Select a named item from a Windows UI Automation control.","parameters":{"type":"OBJECT","properties":{"title":{"type":"STRING"},"item":{"type":"STRING"}},"required":["title","item"]},"handler":windows_ui_control_select}
