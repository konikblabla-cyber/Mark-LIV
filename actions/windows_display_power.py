"""Direct Windows display power control."""
import platform,ctypes
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_display_power(parameters=None,**kwargs):
 p=parameters or {}; action=str(p.get("action","off")).lower()
 if action not in ("off","on"):return "Supported actions: off, on."
 if action=="off": ctypes.windll.user32.SendMessageW(0xFFFF,0x0112,0xF170,2)
 else: ctypes.windll.user32.keybd_event(0x5B,0,0,0);ctypes.windll.user32.keybd_event(0x5B,0,2,0)
 return f"Display power action: {action}."
TOOL={"name":"windows_display_power","description":"Turn Windows display off or wake it using normal Windows APIs.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING","enum":["off","on"]}}},"handler":windows_display_power}
