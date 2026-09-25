"""Wait for Windows network connectivity."""
import platform,time,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_network_wait(parameters=None,**kwargs):
 p=parameters or {}; host=str(p.get("host") or "1.1.1.1").strip(); timeout=max(1,min(int(p.get("timeout",30)),120)); end=time.time()+timeout
 while time.time()<end:
  r=subprocess.run(["ping","-n","1","-w","1000",host],capture_output=True,text=True,encoding="utf-8",errors="replace")
  if r.returncode==0:return f"Network reachable: {host}"
  time.sleep(1)
 return f"Network not reachable within {timeout}s: {host}"
TOOL={"name":"windows_network_wait","description":"Wait until a Windows ping target becomes reachable.","parameters":{"type":"OBJECT","properties":{"host":{"type":"STRING"},"timeout":{"type":"INTEGER"}}},"handler":windows_network_wait}
