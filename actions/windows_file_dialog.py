"""Open standard Windows file/folder dialogs."""
import platform,pyautogui,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_file_dialog(parameters=None,**kwargs):
 p=parameters or {}; action=str(p.get("action","open")).lower()
 if action not in ("open","save","folder"):return "Action must be open, save, or folder."
 pyautogui.hotkey("ctrl","o" if action=="open" else "shift+s" if action=="save" else "l")
 time.sleep(.3)
 return f"Requested standard Windows dialog: {action}."
TOOL={"name":"windows_file_dialog","description":"Request a standard application file/save dialog or a location dialog using normal keyboard input.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}}},"handler":windows_file_dialog}
