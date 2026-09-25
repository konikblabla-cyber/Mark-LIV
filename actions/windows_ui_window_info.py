"""Read-only detailed active-window UI Automation metadata."""
import platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_window_info(parameters=None,**kwargs):
 try:
  from pywinauto import Desktop
  w=Desktop(backend="uia").get_active(); e=w.element_info
  return f"title={w.window_text()}; class={e.class_name}; control_type={e.control_type}; automation_id={e.automation_id}; handle={e.handle}."
 except Exception as e:return f"Window UI inspection failed: {e}"
TOOL={"name":"windows_ui_window_info","description":"Read-only UI Automation metadata for the active Windows window.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_ui_window_info}
