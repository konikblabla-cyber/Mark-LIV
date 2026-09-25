"""Read-only Windows workstation lock state."""
import ctypes,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_screen_lock_state(parameters=None,**kwargs):
 u=ctypes.windll.user32; h=u.OpenInputDesktop(0,False,0x0100)
 return f"Interactive desktop available={bool(h)}; workstation_locked={not bool(h)}."
TOOL={"name":"windows_screen_lock_state","description":"Read-only indication of whether the interactive Windows desktop is available.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_screen_lock_state}
