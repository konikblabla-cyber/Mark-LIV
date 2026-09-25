"""Windows mouse button state diagnostics."""
import ctypes, platform
if platform.system() != "Windows":
    raise RuntimeError("Windows-only.")
VK_LBUTTON=0x01; VK_RBUTTON=0x02; VK_MBUTTON=0x04
def windows_mouse_buttons(parameters=None, **kwargs):
    u=ctypes.windll.user32
    def down(v): return bool(u.GetAsyncKeyState(v) & 0x8000)
    return f"Mouse buttons: left={'down' if down(VK_LBUTTON) else 'up'}, right={'down' if down(VK_RBUTTON) else 'up'}, middle={'down' if down(VK_MBUTTON) else 'up'}."
TOOL={"name":"windows_mouse_buttons","description":"Read-only Windows left, right and middle mouse-button state.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_mouse_buttons}
