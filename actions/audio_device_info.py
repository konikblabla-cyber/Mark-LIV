"""Windows audio endpoint inventory."""
import platform,subprocess
def audio_device_info(parameters=None,**kwargs):
 if platform.system()!="Windows": return "audio_device_info is available only on Windows."
 try:
  r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command","Get-CimInstance Win32_SoundDevice | Select Name,Status,Manufacturer,PNPDeviceID | Format-Table -AutoSize"],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
  return (r.stdout or r.stderr or "No audio devices.")[:10000]
 except (subprocess.TimeoutExpired,OSError) as e:
  return f"Audio device check failed: {e}"
TOOL={"name":"audio_device_info","description":"Read-only Windows sound-device inventory with status and manufacturer.","parameters":{"type":"OBJECT","properties":{}},"handler":audio_device_info}
