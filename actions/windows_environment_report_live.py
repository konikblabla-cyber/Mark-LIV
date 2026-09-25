"""Windows live environment report."""
import os,platform
def windows_environment_report_live(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 names=["COMPUTERNAME","USERNAME","USERPROFILE","TEMP","TMP","APPDATA","LOCALAPPDATA","PROGRAMDATA","PROGRAMFILES","PROGRAMFILES(X86)","WINDIR","PATH"]
 return "\n".join(f"{n}={os.environ.get(n,'<unset>')}" for n in names)
TOOL={"name":"windows_environment_report_live","description":"Read-only live Windows environment paths and identity variables.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_environment_report_live}
