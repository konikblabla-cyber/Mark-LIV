"""Copy selected Windows UI text using normal Ctrl+C."""
import platform,pyautogui,time
def windows_clipboard_copy_action(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 time.sleep(.05);pyautogui.hotkey("ctrl","c");time.sleep(.1);return "Ctrl+C sent to the focused Windows control."
TOOL={"name":"windows_clipboard_copy_action","description":"Send normal Ctrl+C to the currently focused Windows control.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_clipboard_copy_action}
