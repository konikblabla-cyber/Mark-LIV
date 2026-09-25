"""Windows USB device inventory."""
import platform,subprocess
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def windows_usb_inventory(parameters=None,**kwargs):
 cmd="Get-PnpDevice -PresentOnly -ErrorAction SilentlyContinue | Where-Object {$_.InstanceId -like 'USB*'} | Select Status,Class,FriendlyName,InstanceId | Format-Table -AutoSize"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No USB devices.")[:12000]
TOOL={"name":"windows_usb_inventory","description":"Read-only Windows inventory of currently present USB Plug-and-Play devices and their status.","parameters":{"type":"OBJECT","properties":{}},"handler=windows_usb_inventory}
