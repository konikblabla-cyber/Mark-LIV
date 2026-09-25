"""Windows network latency sampler."""
import platform,subprocess,re
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_network_latency(parameters=None,**kwargs):
 p=parameters or {}; host=str(p.get("host","1.1.1.1")).strip(); count=max(1,min(int(p.get("count",5)),20))
 if not host or any(c in host for c in "\r\n;&|<>"):return "Invalid host."
 r=subprocess.run(["ping","-n",str(count),"-w","1500",host],capture_output=True,text=True,timeout=count*2+5,creationflags=subprocess.CREATE_NO_WINDOW)
 out=(r.stdout or r.stderr).strip(); vals=re.findall(r"(?:Average|Średnia) = (\d+)ms",out,re.I)
 return f"{host}: {'ONLINE' if r.returncode==0 else 'OFFLINE'}\n"+(f"Average latency: {vals[-1]} ms" if vals else out[-2000:])
TOOL={"name":"windows_network_latency","description":"Read-only Windows ping latency measurement for a host.","parameters":{"type":"OBJECT","properties":{"host":{"type":"STRING"},"count":{"type":"INTEGER"}}},"handler":windows_network_latency}
