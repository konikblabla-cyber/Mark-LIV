"""Windows USB device inventory."""
import platform,subprocess
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def windows_usb_info(parameters=None,**kwargs):
 cmd="Get-PnpDevice -Class USB -ErrorAction SilentlyContinue | Select Status,Class,FriendlyName,InstanceId | Format-Table -AutoSize"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No USB devices.")[:12000]
TOOL={"name":"windows_usb_info","description":"Read-only Windows USB device inventory with status and device identifiers.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_usb_info}
