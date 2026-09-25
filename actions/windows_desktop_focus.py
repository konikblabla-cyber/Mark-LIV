"""Focus the Windows desktop shell."""
import ctypes,platform,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_desktop_focus(parameters=None,**kwargs):
 pyautogui.hotkey("win","d")
 return "Windows desktop focused."
TOOL={"name":"windows_desktop_focus","description":"Bring the Windows desktop to the foreground using normal Win+D input.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_desktop_focus}
