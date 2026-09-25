"""Switch Windows to a power-saving plan."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_battery_mode(parameters=None,**kwargs):
 r=subprocess.run(["powercfg","/setactive","SCHEME_MAX"],capture_output=True,text=True,timeout=15)
 return "Power Saver plan activated." if r.returncode==0 else f"Power Saver failed: {r.stderr.strip() or 'unknown error'}"
TOOL={"name":"windows_battery_mode","description":"Activate the Windows Power Saver power plan.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_battery_mode}
