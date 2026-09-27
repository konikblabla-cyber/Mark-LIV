"""Select an item in an accessible Windows combo/list control."""
import platform
from core.permissions import permission_decision
from core import confirm
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_select(parameters=None,**kwargs):
             if not kwargs.get("_permission_token"):
                 p=dict(parameters or {})
                 d,r=permission_decision("windows_ui_select",p)
                 if d=="deny": return f"Permission denied: {r}"
                 if d=="confirm":
                     return confirm.request(key="windows_ui_select",title="Allow JARVIS: windows_ui_select?",detail=f"{r}. Waiting for your confirmation.",run=lambda: windows_ui_select(p,_permission_token=True))
    p=parameters or {}; control=str(p.get("control") or "").strip(); item=str(p.get("item") or "").strip()
    if not control or not item:return "Missing control or item."
    try:
        from pywinauto import Desktop
        w=Desktop(backend="uia").get_active(); cs=w.descendants(title=control)
        if len(cs)!=1:return f"Expected exactly one control named '{control}', found {len(cs)}."
        c=cs[0]
        try:c.select(item)
        except Exception:c.child_window(title=item).click_input()
        return f"Selected '{item}' in '{control}'."
    except Exception as e:return f"UI selection failed: {e}"
TOOL={"name":"windows_ui_select","description":"Select an item in one uniquely named accessible Windows combo box or list control.","parameters":{"type":"OBJECT","properties":{"control":{"type":"STRING"},"item":{"type":"STRING"}},"required":["control","item"]},"handler":windows_ui_select}
