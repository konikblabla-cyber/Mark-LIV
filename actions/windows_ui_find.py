"""Find Windows UI Automation controls by title/name."""
import platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_find(parameters=None,**kwargs):
    p=parameters or {}; title=str(p.get("window") or "").strip(); control=str(p.get("control") or "").strip()
    if not title or not control:return "Provide window and control text."
    try:
        from pywinauto import Desktop
        wins=Desktop(backend="uia").windows(title_re=f".*{title}.*")
        if not wins:return f"Window not found: {title}"
        w=wins[0]; matches=w.descendants(title_re=f".*{control}.*")
        return "\n".join(f"{x.window_text()} | {x.friendly_class_name()}" for x in matches[:30]) or f"Control not found: {control}"
    except Exception as e:return f"UI Automation error: {e}"
TOOL={"name":"windows_ui_find","description":"Find visible Windows UI Automation controls inside a window by title text.","parameters":{"type":"OBJECT","properties":{"window":{"type":"STRING"},"control":{"type":"STRING"}},"required":["window","control"]},"handler":windows_ui_find}
