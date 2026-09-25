"""Windows Defender read-only configuration summary."""
import platform,subprocess
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def windows_defender_info(parameters=None,**kwargs):
 cmd="Get-MpComputerStatus | Select AMServiceEnabled,AntivirusEnabled,RealTimeProtectionEnabled,BehaviorMonitorEnabled,AntivirusSignatureVersion,QuickScanAge,FullScanAge | Format-List"
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or "Defender information unavailable.")[:8000]
TOOL={"name":"windows_defender_info","description":"Read-only Windows Defender status, real-time protection and signature/scan-age information.","parameters":{"type":"OBJECT","properties":{}},"handler=windows_defender_info}
