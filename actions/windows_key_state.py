"""Read-only Windows modifier-key state."""
import ctypes,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
VK_SHIFT=0x10;VK_CONTROL=0x11;VK_MENU=0x12;VK_LWIN=0x5B;VK_RWIN=0x5C
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_key_state(parameters=None,**kwargs):
 u=ctypes.windll.user32
 def down(v): return bool(u.GetAsyncKeyState(v)&0x8000)
 return f"Shift={'down' if down(VK_SHIFT) else 'up'}, Ctrl={'down' if down(VK_CONTROL) else 'up'}, Alt={'down' if down(VK_MENU) else 'up'}, Win={'down' if (down(VK_LWIN) or down(VK_RWIN)) else 'up'}."
TOOL={"name":"windows_key_state","description":"Read-only state of Shift, Ctrl, Alt and Windows modifier keys.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_key_state}
