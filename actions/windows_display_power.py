"""Direct Windows display power control."""
import platform,ctypes

def windows_display_power(parameters=None,**kwargs):
    if platform.system()!="Windows": return "Windows-only action."
    p=parameters or {}; action=str(p.get("action","off")).lower()
    if action not in ("off","on"): return "Supported actions: off, on."
    u=ctypes.windll.user32
    if action=="off": u.SendMessageW(0xFFFF,0x0112,0xF170,2)
    else: u.SendMessageW(0xFFFF,0x0112,0xF170,-1)
    return f"Display power action: {action}."

TOOL={"name":"windows_display_power","description":"Turn Windows display off or request wake using the standard monitor-power message.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING","enum":["off","on"]}}},"handler":windows_display_power}
