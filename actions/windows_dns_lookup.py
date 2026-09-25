"""Windows DNS lookup helper."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_dns_lookup(parameters=None,**kwargs):
 p=parameters or {}; host=str(p.get("host","")).strip()
 if not host or len(host)>253 or any(c in host for c in "\r\n;&|<>"):return "Valid hostname is required."
 r=subprocess.run(["nslookup",host],capture_output=True,text=True,timeout=10,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "DNS lookup failed.")[:6000]
TOOL={"name":"windows_dns_lookup","description":"Read-only Windows DNS lookup for a hostname.","parameters":{"type":"OBJECT","properties":{"host":{"type":"STRING"}},"required":["host"]},"handler":windows_dns_lookup}
