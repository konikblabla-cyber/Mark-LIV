"""Focus the Windows desktop shell."""
import ctypes,platform,pyautogui
def windows_desktop_focus(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 pyautogui.hotkey("win","d")
 return "Windows desktop focused."
TOOL={"name":"windows_desktop_focus","description":"Bring the Windows desktop to the foreground using normal Win+D input.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_desktop_focus}
