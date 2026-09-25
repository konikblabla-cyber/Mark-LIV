"""Windows process network-connection inventory."""
import platform,subprocess
def process_network_usage(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}
 try: pid=int(p.get("pid",0))
 except (TypeError,ValueError): return "Valid PID required."
 cmd="Get-NetTCPConnection -ErrorAction SilentlyContinue | Select OwningProcess,State,LocalAddress,LocalPort,RemoteAddress,RemotePort | Sort OwningProcess | Format-Table -AutoSize"
 if pid>0:cmd=f"Get-NetTCPConnection -OwningProcess {pid} -ErrorAction SilentlyContinue | Select OwningProcess,State,LocalAddress,LocalPort,RemoteAddress,RemotePort | Format-Table -AutoSize"
 try:
  r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 except (subprocess.TimeoutExpired,OSError) as e: return f"Network inventory failed: {e}"
 return (r.stdout or r.stderr or "No network connections.")[:12000]
TOOL={"name":"process_network_usage","description":"Read-only Windows TCP connection inventory, optionally filtered by process PID.","parameters":{"type":"OBJECT","properties":{"pid":{"type":"INTEGER"}},"required":["pid"]},"handler":process_network_usage}
