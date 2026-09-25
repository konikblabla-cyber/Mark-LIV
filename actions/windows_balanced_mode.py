"""Restore the Windows Balanced power plan."""
import platform,subprocess
def windows_balanced_mode(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 r=subprocess.run(["powercfg","/setactive","SCHEME_BALANCED"],capture_output=True,text=True,timeout=15)
 return "Balanced power plan activated." if r.returncode==0 else f"Balanced plan failed: {r.stderr.strip() or 'unknown error'}"
TOOL={"name":"windows_balanced_mode","description":"Restore the standard Windows Balanced power plan.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_balanced_mode}
