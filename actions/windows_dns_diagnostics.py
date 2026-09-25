"""Windows DNS diagnostics."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_dns_diagnostics(parameters=None,**kwargs):
 p=parameters or {}; host=str(p.get("host","example.com")).strip() or "example.com"
 if len(host)>253 or any(c in host for c in "\r\n;&|<>"): return "Invalid host."
 cmd=f"Resolve-DnsName -Name '{host}' -ErrorAction SilentlyContinue | Select Name,Type,IPAddress,NameHost | Format-Table -AutoSize"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "DNS lookup failed.")[:10000]
TOOL={"name":"windows_dns_diagnostics","description":"Read-only Windows DNS lookup for a hostname.","parameters":{"type":"OBJECT","properties":{"host":{"type":"STRING"}}},"handler":windows_dns_diagnostics}
