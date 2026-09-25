"""Windows notification-area interaction via normal UI input."""
import platform,pyautogui,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_tray_action(parameters=None,**kwargs):
 p=parameters or {}; action=str(p.get("action","open")).lower()
 if action=="open":
  pyautogui.hotkey("win","b");time.sleep(.2);pyautogui.press("enter")
 elif action=="show_hidden":
  pyautogui.hotkey("win","b");time.sleep(.2);pyautogui.press("enter")
 else:return "Action must be open or show_hidden."
 return f"Requested Windows notification-area interaction: {action}."
TOOL={"name":"windows_tray_action","description":"Use normal Windows keyboard navigation to reach the notification area.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}}},"handler":windows_tray_action}
