"""Inspect standard Windows UI controls in the foreground window."""
import platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_controls(parameters=None,**kwargs):
    try:
        from pywinauto import Desktop
        win=Desktop(backend="uia").get_active()
        rows=[]
        for c in win.descendants(depth=3)[:100]:
            try:
                name=c.window_text()
                if name or c.element_info.control_type:
                    rows.append(f"{c.element_info.control_type}: {name or '<unnamed>'}")
            except Exception: pass
        return "\n".join(rows) if rows else "No accessible UI controls found."
    except Exception as e: return f"UI inspection failed: {e}"
TOOL={"name":"windows_ui_controls","description":"Inspect accessible controls in the active Windows window using UI Automation.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_ui_controls}
