"""Windows route lookup for a destination."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_route_lookup(parameters=None,**kwargs):
 p=parameters or {}; host=str(p.get("host","1.1.1.1")).strip()
 if not host or any(c in host for c in "\r\n;&|<>"):return "Invalid destination."
 r=subprocess.run(["tracert","-d","-h","12","-w","1000",host],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "Route lookup failed.")[:10000]
TOOL={"name":"windows_route_lookup","description":"Read-only Windows traceroute to a destination for diagnosing network paths.","parameters":{"type":"OBJECT","properties":{"host":{"type":"STRING"}},"required":["host"]},"handler":windows_route_lookup}
