"""Open standard Windows file dialogs safely."""
import platform,pyautogui,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_file_dialog(parameters=None,**kwargs):
    p=parameters or {}; action=str(p.get("action","open")).lower()
    if action=="open":
        pyautogui.hotkey("ctrl","o")
    elif action=="save":
        pyautogui.hotkey("ctrl","shift","s")
    elif action=="folder":
        pyautogui.hotkey("win","e")
    else:
        return "Action must be open, save, or folder."
    time.sleep(.3)
    return f"Requested Windows {action} workflow."
TOOL={"name":"windows_file_dialog","description":"Open a standard application open/save dialog, or Windows File Explorer for folder selection, using normal keyboard input.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING","enum":["open","save","folder"]}}},"handler":windows_file_dialog}
