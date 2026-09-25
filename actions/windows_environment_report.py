"""Windows environment report for Mark-LIV."""
import platform,os
def windows_environment_report(parameters=None,**kwargs):
 if platform.system()!="Windows":raise RuntimeError("Windows-only.")
 keys=["COMPUTERNAME","USERNAME","USERDOMAIN","PROCESSOR_ARCHITECTURE","NUMBER_OF_PROCESSORS","TEMP","SystemRoot","ProgramFiles","LOCALAPPDATA"]
 return "\n".join(f"{k}={os.environ.get(k,'')}" for k in keys)
TOOL={"name":"windows_environment_report","description":"Read-only Windows environment identity and key system paths useful for diagnostics.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_environment_report}
