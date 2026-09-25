"""Read-only Windows keyboard layout information."""
import platform,ctypes

def windows_keyboard_layout(parameters=None,**kwargs):
 if platform.system()!="Windows":return "Windows-only action."
 try:
  u=ctypes.windll.user32;h=u.GetKeyboardLayout(0)
  if not h:return "Unable to read current keyboard layout."
  return f"Current keyboard layout LANGID: 0x{h&0xffff:04x}."
 except (AttributeError,OSError):return "Unable to read Windows keyboard layout."
TOOL={"name":"windows_keyboard_layout","description":"Read-only current Windows keyboard layout LANGID.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_keyboard_layout}