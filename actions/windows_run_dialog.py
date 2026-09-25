"""Windows Run dialog helper."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_run_dialog(parameters=None,**kwargs):
 p=parameters or {}; command=str(p.get("command","")).strip()
 if not command:return "Command is required."
 # Opens Run and types the requested command; Windows/UAC remain in control.
 safe=command.replace("'", "''")
 ps=f"$ws=New-Object -ComObject WScript.Shell;$ws.SendKeys('%{{F2}}');Start-Sleep -Milliseconds 250;$ws.SendKeys('{safe}');$ws.SendKeys('{{ENTER}}')"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",ps],capture_output=True,text=True,timeout=10,creationflags=subprocess.CREATE_NO_WINDOW)
 return "Run dialog command submitted." if r.returncode==0 else (r.stderr or "Run dialog failed.")
TOOL={"name":"windows_run_dialog","description":"Type a command into the normal Windows Run dialog and submit it; does not bypass UAC or security prompts.","parameters":{"type":"OBJECT","properties":{"command":{"type":"STRING"}},"required":["command"]},"handler":windows_run_dialog}
