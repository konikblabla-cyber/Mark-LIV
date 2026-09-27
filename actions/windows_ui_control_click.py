"""Click a uniquely identified Windows UI Automation control."""
import platform
from core.permissions import permission_decision
from core import confirm
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_control_click(parameters=None,**kwargs):
    if not kwargs.get("_permission_token"):
        p=dict(parameters or {})
        d,r=permission_decision("windows_ui_control_click",p)
        if d=="deny": return f"Permission denied: {r}"
        if d=="confirm":
            return confirm.request(key="windows_ui_control_click",title="Allow JARVIS: windows_ui_control_click?",detail=f"{r}. Waiting for your confirmation.",run=lambda: windows_ui_control_click(p,_permission_token=True))
    p=parameters or {}; title=str(p.get("title") or "").strip()
    if not title:return "Missing control title."
    try:
        from pywinauto import Desktop
        win=Desktop(backend="uia").get_active()
        c=win.child_window(title=title)
        if c.exists(timeout=2):
            c.click_input(); return f"Clicked UI control: {title}"
        return f"Control not found: {title}"
    except Exception as e:return f"UI click failed: {e}"
TOOL={"name":"windows_ui_control_click","description":"Click a uniquely named accessible control in the active Windows window.","parameters":{"type":"OBJECT","properties":{"title":{"type":"STRING"}},"required":["title"]},"handler":windows_ui_control_click}
