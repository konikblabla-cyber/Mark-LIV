"""Send Escape to the focused Windows control."""
import platform,pyautogui
def windows_escape_action(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 pyautogui.press("esc");return "Escape sent."
TOOL={"name":"windows_escape_action","description":"Send Escape to the focused Windows control using normal keyboard input.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_escape_action}
