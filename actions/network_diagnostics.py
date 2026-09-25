"""Windows network diagnostics bundle for Mark-LIV."""
import platform,subprocess
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def network_diagnostics(parameters=None,**kwargs):
 p=parameters or {}; a=str(p.get("action","quick")).lower().strip()
 cmds={"quick":["ipconfig","/flushdns"],"config":["ipconfig","/all"],"routes":["route","print"],"dns":["nslookup","example.com"],"arp":["arp","-a"]}
 if a not in cmds:return "Use quick, config, routes, dns or arp."
 c=cmds[a]; r=subprocess.run(c,capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or f"Exit code: {r.returncode}")[:12000]
TOOL={"name":"network_diagnostics","description":"Windows-only network diagnostic bundle: IP configuration, routing, DNS lookup, ARP table, or DNS-cache refresh.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}},"required":["action"]},"handler":network_diagnostics}
