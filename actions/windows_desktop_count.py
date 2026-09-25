"""Read-only Windows virtual desktop count."""
import platform,subprocess
def windows_desktop_count(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 r=subprocess.run(["powershell","-NoProfile","-Command","(Get-ItemProperty 'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\SessionInfo\*' -ErrorAction SilentlyContinue | Measure-Object).Count"],capture_output=True,text=True,timeout=10)
 return "Virtual desktop registry entries: "+r.stdout.strip()
TOOL={"name":"windows_desktop_count","description":"Read-only estimate of Windows virtual desktop registry entries.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_desktop_count}
