"""Read-only Windows clipboard availability."""
import ctypes,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_clipboard_state(parameters=None,**kwargs):
 u=ctypes.windll.user32
 if not u.OpenClipboard(0): return "Clipboard is currently unavailable or locked."
 try:
  return f"Clipboard has text={bool(u.IsClipboardFormatAvailable(13))}; bitmap={bool(u.IsClipboardFormatAvailable(2))}; files={bool(u.IsClipboardFormatAvailable(15))}."
 finally:u.CloseClipboard()
TOOL={"name":"windows_clipboard_state","description":"Read-only Windows clipboard format availability without returning clipboard contents.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_clipboard_state}
