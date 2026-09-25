"""Read-only Windows environment variable inspector."""
import platform,os
def windows_environment_variables(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 p=parameters or {}; prefix=str(p.get("prefix","")).strip().upper()
 rows=[]
 for k,v in sorted(os.environ.items()):
  if prefix and not k.upper().startswith(prefix):continue
  rows.append(f"{k}={v}")
  if len(rows)>=200:break
 return "\n".join(rows) or "No matching environment variables."
TOOL={"name":"windows_environment_variables","description":"Read-only inspection of Windows process environment variables, optionally filtered by prefix.","parameters":{"type":"OBJECT","properties":{"prefix":{"type":"STRING"}}},"handler":windows_environment_variables}
