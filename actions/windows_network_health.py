"""Windows multi-endpoint network health check."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_network_health(parameters=None,**kwargs):
 p=parameters or {}; hosts=p.get("hosts",["1.1.1.1","8.8.8.8"]); hosts=hosts if isinstance(hosts,list) else ["1.1.1.1","8.8.8.8"]; hosts=[str(x) for x in hosts[:5]]
 rows=[]
 for h in hosts:
  if len(h)>253 or any(c in h for c in "\r\n;&|<>"): continue
  r=subprocess.run(["ping","-n","2","-w","1500",h],capture_output=True,text=True,timeout=6,creationflags=subprocess.CREATE_NO_WINDOW)
  rows.append(f"{h}: {'ONLINE' if r.returncode==0 else 'OFFLINE'}\n{(r.stdout or r.stderr).strip()[-1200:]}")
 return "\n\n".join(rows) or "No valid hosts."
TOOL={"name":"windows_network_health","description":"Windows read-only connectivity test against multiple hosts to distinguish general network reachability.","parameters":{"type":"OBJECT","properties":{"hosts":{"type":"ARRAY","items":{"type":"STRING"}}}},"handler":windows_network_health}
