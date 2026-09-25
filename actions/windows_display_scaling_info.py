"""Read-only Windows display scaling information."""
import platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_display_scaling_info(parameters=None,**kwargs):
 try:
  import winreg
  k=winreg.OpenKey(winreg.HKEY_CURRENT_USER,r"Control Panel\Desktop");v,_=winreg.QueryValueEx(k,"LogPixels");winreg.CloseKey(k)
  return f"Display DPI: {v}; scaling: {round(v/96*100)}%."
 except Exception as e:return f"Display scaling unavailable: {e}"
TOOL={"name":"windows_display_scaling_info","description":"Read-only Windows display DPI and scaling setting.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_display_scaling_info}
