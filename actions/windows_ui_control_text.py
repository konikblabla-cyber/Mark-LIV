"""Set text in a uniquely identified Windows UI Automation control."""
import platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_control_text(parameters=None,**kwargs):
    p=parameters or {}; title=str(p.get("title") or "").strip(); value=str(p.get("text") or "")
    if not title:return "Missing control title."
    try:
        from pywinauto import Desktop
        win=Desktop(backend="uia").get_active(); c=win.child_window(title=title)
        if not c.exists(timeout=2): return f"Control not found: {title}"
        c.set_edit_text(value); return f"Text entered into: {title}"
    except Exception as e:return f"UI text entry failed: {e}"
TOOL={"name":"windows_ui_control_text","description":"Set text in a uniquely identified editable Windows UI Automation control.","parameters":{"type":"OBJECT","properties":{"title":{"type":"STRING"},"text":{"type":"STRING"}},"required":["title","text"]},"handler":windows_ui_control_text}
