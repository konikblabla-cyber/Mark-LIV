"""Open allowlisted Windows URI schemes."""
import os,platform
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
ALLOWED=("ms-settings:","ms-screenclip:","ms-calculator:","ms-clock:","mailto:","tel:")
def windows_uri_open(parameters=None,**kwargs):
 uri=str((parameters or {}).get("uri","")).strip()
 if not uri:return "Missing URI."
 if not uri.lower().startswith(ALLOWED):return "URI scheme is not allowed."
 os.startfile(uri);return f"Opened Windows URI: {uri}"
TOOL={"name":"windows_uri_open","description":"Open an allowlisted Windows URI such as ms-settings or mailto using normal Windows handling.","parameters":{"type":"OBJECT","properties":{"uri":{"type":"STRING"}},"required":["uri"]},"handler":windows_uri_open}
