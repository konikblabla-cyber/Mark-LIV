"""Open built-in Windows diagnostic interfaces."""
import platform,subprocess
def windows_diagnostic_tools(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; action=str(p.get("action","")).lower()
 commands={"directx":"dxdiag.exe","system_information":"msinfo32.exe","memory_diagnostic":"mdsched.exe","network_troubleshooter":"msdt.exe"}
 if action not in commands:return "Action must be directx, system_information, memory_diagnostic, or network_troubleshooter."
 try:
  subprocess.Popen([commands[action]],creationflags=subprocess.CREATE_NO_WINDOW)
 except OSError as e:return f"Failed to start diagnostic tool: {e}"
 return f"Started Windows diagnostic tool: {action}."
TOOL={"name":"windows_diagnostic_tools","description":"Start built-in Windows DirectX Diagnostic, System Information, Memory Diagnostic, or network troubleshooting tool.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}},"required":["action"]},"handler":windows_diagnostic_tools}
