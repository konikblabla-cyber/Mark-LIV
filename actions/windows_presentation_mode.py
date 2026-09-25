"""Prepare Windows for a presentation."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_presentation_mode(parameters=None,**kwargs):
 cmds=[["powercfg","/change","monitor-timeout-ac", "0"],["powercfg","/change","standby-timeout-ac","0"]]
 ok=0
 for c in cmds:
  try:
   if subprocess.run(c,capture_output=True,timeout=10).returncode==0: ok+=1
  except Exception: pass
 return "Presentation mode enabled: display sleep and system standby disabled while on AC power." if ok==2 else f"Presentation mode partially applied ({ok}/2 settings)."
TOOL={"name":"windows_presentation_mode","description":"Temporarily prepare Windows for a presentation by preventing display sleep and standby on AC power.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_presentation_mode}
