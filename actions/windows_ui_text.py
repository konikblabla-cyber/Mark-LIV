"""Set text in a Windows UI Automation edit control."""
import platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_text(parameters=None,**kwargs):
    p=parameters or {}; title=str(p.get("window") or "").strip(); control=str(p.get("control") or "").strip(); value=str(p.get("text") or "")
    if not title or not control:return "Provide window and control text."
    if len(value)>5000:return "Text too long (max 5000 characters)."
    try:
        from pywinauto import Desktop
        wins=Desktop(backend="uia").windows(title_re=f".*{title}.*")
        if not wins:return f"Window not found: {title}"
        matches=wins[0].descendants(title_re=f"^{control}$")
        if len(matches)!=1:return f"Expected one matching control, found {len(matches)}."
        matches[0].set_edit_text(value)
        return f"Text set in control: {control}"
    except Exception as e:return f"UI text error: {e}"
TOOL={"name":"windows_ui_text","description":"Set text in exactly one visible Windows UI Automation edit control.","parameters":{"type":"OBJECT","properties":{"window":{"type":"STRING"},"control":{"type":"STRING"},"text":{"type":"STRING"}},"required":["window","control","text"]},"handler":windows_ui_text}
