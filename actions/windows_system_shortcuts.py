"""Common Windows shell shortcuts."""
import platform,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
S={"explorer":["win","e"],"settings":["win","i"],"search":["win","s"],"run":["win","r"],"lock":["win","l"]}
def windows_system_shortcuts(parameters=None,**kwargs):
 a=str((parameters or {}).get("action","")).lower()
 if a not in S:return "Supported: explorer, settings, search, run, lock."
 pyautogui.hotkey(*S[a]);return f"Windows shortcut executed: {a}."
TOOL={"name":"windows_system_shortcuts","description":"Open common Windows shell surfaces with normal shortcuts.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}},"required":["action"]},"handler":windows_system_shortcuts}
