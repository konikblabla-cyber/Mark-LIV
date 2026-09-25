"""Wait for a TCP port on Windows to become reachable."""
import platform,time,socket
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_port_wait(parameters=None,**kwargs):
 p=parameters or {};host=str(p.get("host","127.0.0.1")).strip();port=max(1,min(int(p.get("port",80)),65535));timeout=max(1,min(int(p.get("timeout",30)),120))
 end=time.time()+timeout
 while time.time()<end:
  try:
   with socket.create_connection((host,port),timeout=.5):return f"TCP port reachable: {host}:{port}"
  except OSError:time.sleep(.5)
 return f"TCP port not reachable after {timeout}s: {host}:{port}"
TOOL={"name":"windows_port_wait","description":"Wait for a TCP service on a host and port to become reachable.","parameters":{"type":"OBJECT","properties":{"host":{"type":"STRING"},"port":{"type":"INTEGER"},"timeout":{"type":"INTEGER"}},"required":["port"]},"handler":windows_port_wait}
