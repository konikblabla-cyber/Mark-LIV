"""Windows keyboard lock-key state diagnostics."""
import ctypes, platform
if platform.system() != "Windows":
    raise RuntimeError("Windows-only.")
VK_CAPITAL=0x14; VK_NUMLOCK=0x90; VK_SCROLL=0x91
def windows_lock_state(parameters=None, **kwargs):
    u=ctypes.windll.user32
    def on(v): return bool(u.GetKeyState(v) & 1)
    return f"CapsLock={'on' if on(VK_CAPITAL) else 'off'}, NumLock={'on' if on(VK_NUMLOCK) else 'off'}, ScrollLock={'on' if on(VK_SCROLL) else 'off'}."
TOOL={"name":"windows_lock_state","description":"Read-only Windows Caps Lock, Num Lock and Scroll Lock state.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_lock_state}
