"""Click a uniquely matched Windows UI Automation control."""
import platform
from core.permissions import permission_decision
from core import confirm
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_element_click(parameters=None,**kwargs):
    if not kwargs.get("_permission_token"):
        p=dict(parameters or {})
        d,r=permission_decision("windows_ui_element_click",p)
        if d=="deny": return f"Permission denied: {r}"
        if d=="confirm":
            return confirm.request(key="windows_ui_element_click",title="Allow JARVIS: windows_ui_element_click?",detail=f"{r}. Waiting for your confirmation.",run=lambda: windows_ui_element_click(p,_permission_token=True))
    p=parameters or {}; title=str(p.get("title") or "").strip()
    if not title:return "Missing control title."
    try:
        from pywinauto import Desktop
        matches=[]
        for w in Desktop(backend="uia").windows():
            try:
                for c in w.descendants():
                    if str(c.window_text() or "")==title: matches.append(c)
            except Exception: pass
        if len(matches)!=1:return f"Expected one matching control, found {len(matches)}."
        matches[0].click_input()
        return f"Clicked UI control '{title}'."
    except Exception as e:return f"UIA click failed: {e}"
TOOL={"name":"windows_ui_element_click","description":"Click a uniquely matched visible Windows UI Automation control by exact title.","parameters":{"type":"OBJECT","properties":{"title":{"type":"STRING"}},"required":["title"]},"handler":windows_ui_element_click}
