"""Common Windows shell shortcuts."""
import platform,pyautogui
from core.permissions import permission_decision
from core import confirm
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
S={"explorer":["win","e"],"settings":["win","i"],"search":["win","s"],"run":["win","r"],"lock":["win","l"]}
def windows_system_shortcuts(parameters=None,**kwargs):
 if not kwargs.get("_permission_token"):
  p=dict(parameters or {});d,r=permission_decision("windows_system_shortcuts",p)
  if d=="deny":return f"Permission denied: {r}"
  if d=="confirm":return confirm.request(key="windows_system_shortcuts",title="Allow JARVIS: windows_system_shortcuts?",detail=f"{r}. Waiting for your confirmation.",run=lambda:windows_system_shortcuts(p,_permission_token=True))
 a=str(p.get("action","")).lower()
 if a not in S:return "Supported: explorer, settings, search, run, lock."
 pyautogui.hotkey(*S[a]);return f"Windows shortcut executed: {a}."
TOOL={"name":"windows_system_shortcuts","description":"Open common Windows shell surfaces with normal shortcuts.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}},"required":["action"]},"handler":windows_system_shortcuts}