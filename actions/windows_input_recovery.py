"""Recover common Windows UI input focus without bypassing security."""
import ctypes,platform,pyautogui,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_input_recovery(parameters=None,**kwargs):
 p=parameters or {}; target=str(p.get("title_contains") or "").strip()
 if target:
  u=ctypes.windll.user32
  # Normal Alt+Tab cycle; no forced injection into protected dialogs.
  pyautogui.hotkey("alt","tab");time.sleep(.25)
  n=u.GetWindowTextLengthW(u.GetForegroundWindow());b=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(u.GetForegroundWindow(),b,n+1)
  return f"Focus recovery attempted; active window='{b.value}'."
 pyautogui.hotkey("esc");return "Focus recovery: sent Escape to the active window."
TOOL={"name":"windows_input_recovery","description":"Recover from common UI focus mistakes using normal Windows input; never bypasses UAC or security dialogs.","parameters":{"type":"OBJECT","properties":{"title_contains":{"type":"STRING"}}},"handler":windows_input_recovery}
