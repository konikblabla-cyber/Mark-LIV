"""Read-only Windows keyboard layout information."""
import platform,ctypes
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_keyboard_layout(parameters=None,**kwargs):
 u=ctypes.windll.user32; h=u.GetKeyboardLayout(0); lang=h&0xffff
 return f"Current keyboard layout LANGID: 0x{lang:04x}."
TOOL={"name":"windows_keyboard_layout","description":"Read-only current Windows keyboard layout LANGID.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_keyboard_layout}
