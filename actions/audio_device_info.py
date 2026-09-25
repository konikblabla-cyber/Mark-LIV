"""Windows audio endpoint inventory."""
import platform,subprocess
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def audio_device_info(parameters=None,**kwargs):
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command","Get-CimInstance Win32_SoundDevice | Select Name,Status,Manufacturer,PNPDeviceID | Format-Table -AutoSize"],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "No audio devices.")[:10000]
TOOL={"name":"audio_device_info","description":"Read-only Windows sound-device inventory with status and manufacturer.","parameters":{"type":"OBJECT","properties":{}},"handler":audio_device_info}
