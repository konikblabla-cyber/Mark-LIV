"""Open built-in Windows administrative tools."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_system_tools(parameters=None,**kwargs):
 p=parameters or {}; action=str(p.get("action","")).lower()
 commands={"event_viewer":"eventvwr.msc","resource_monitor":"resmon.exe","performance_monitor":"perfmon.exe","disk_management":"diskmgmt.msc"}
 if action not in commands:return "Action must be event_viewer, resource_monitor, performance_monitor, or disk_management."
 subprocess.Popen(["cmd","/c","start","",commands[action]],creationflags=subprocess.CREATE_NO_WINDOW)
 return f"Opened Windows system tool: {action}."
TOOL={"name":"windows_system_tools","description":"Open built-in Windows Event Viewer, Resource Monitor, Performance Monitor, or Disk Management.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}},"required":["action"]},"handler":windows_system_tools}
