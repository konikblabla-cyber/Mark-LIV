"""Set text in a uniquely matching Windows UI Automation control."""
import platform
from core.permissions import permission_decision
from core import confirm
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_set_text(parameters=None,**kwargs):
    if not kwargs.get("_permission_token"):
        p=dict(parameters or {})
        d,r=permission_decision("windows_ui_set_text",p)
        if d=="deny": return f"Permission denied: {r}"
        if d=="confirm":
            return confirm.request(key="windows_ui_set_text",title="Allow JARVIS: windows_ui_set_text?",detail=f"{r}. Waiting for your confirmation.",run=lambda: windows_ui_set_text(p,_permission_token=True))
    p=parameters or {}; name=str(p.get("name") or "").strip(); value=str(p.get("text") or "")
    if not name:return "Missing control name."
    try:
        from pywinauto import Desktop
        matches=[]
        for w in Desktop(backend="uia").windows(visible_only=True):
            for c in w.descendants():
    if c.window_text().strip().lower()==name.lower() and hasattr(c,"set_edit_text"): matches.append(c)
        if len(matches)!=1:return f"Expected exactly one editable control, found {len(matches)}."
        matches[0].set_edit_text(value); return f"Text set in control: {name}"
    except Exception as e:return f"UI text entry failed: {e}"
TOOL={"name":"windows_ui_set_text","description":"Set text in one uniquely matched visible Windows UI Automation edit control.","parameters":{"type":"OBJECT","properties":{"name":{"type":"STRING"},"text":{"type":"STRING"}},"required":["name","text"]},"handler":windows_ui_set_text}
