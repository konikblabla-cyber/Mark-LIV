"""Click a Windows UI Automation control by visible title."""
import platform
from core.permissions import permission_decision
from core import confirm
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_click(parameters=None,**kwargs):
    if not kwargs.get("_permission_token"):
        p=dict(parameters or {})
        d,r=permission_decision("windows_ui_click",p)
        if d=="deny": return f"Permission denied: {r}"
        if d=="confirm":
            return confirm.request(key="windows_ui_click",title="Allow JARVIS: windows_ui_click?",detail=f"{r}. Waiting for your confirmation.",run=lambda: windows_ui_click(p,_permission_token=True))
    p=parameters or {}; title=str(p.get("window") or "").strip(); control=str(p.get("control") or "").strip()
    if not title or not control:return "Provide window and control text."
    try:
        from pywinauto import Desktop
        wins=Desktop(backend="uia").windows(title_re=f".*{title}.*")
        if not wins:return f"Window not found: {title}"
        matches=wins[0].descendants(title_re=f"^{control}$")
        if len(matches)!=1:return f"Expected one matching control, found {len(matches)}."
        matches[0].click_input()
        return f"Clicked control: {control}"
    except Exception as e:return f"UI click error: {e}"
TOOL={"name":"windows_ui_click","description":"Click exactly one visible Windows UI Automation control by its displayed title.","parameters":{"type":"OBJECT","properties":{"window":{"type":"STRING"},"control":{"type":"STRING"}},"required":["window","control"]},"handler":windows_ui_click}
