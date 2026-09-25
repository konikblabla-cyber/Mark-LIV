"""Read visible text from Windows UI Automation controls."""
import platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_read(parameters=None,**kwargs):
    p=parameters or {}; title=str(p.get("window") or "").strip()
    if not title:return "Provide window title text."
    try:
        from pywinauto import Desktop
        wins=Desktop(backend="uia").windows(title_re=f".*{title}.*")
        if not wins:return f"Window not found: {title}"
        texts=[]
        for x in wins[0].descendants():
            t=x.window_text()
            if t:texts.append(t)
        return "\n".join(dict.fromkeys(texts))[:8000] or "No visible control text found."
    except Exception as e:return f"UI read error: {e}"
TOOL={"name":"windows_ui_read","description":"Read visible control text from a Windows window through UI Automation.","parameters":{"type":"OBJECT","properties":{"window":{"type":"STRING"}},"required":["window"]},"handler":windows_ui_read}
