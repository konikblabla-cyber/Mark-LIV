"""Windows low-disk-space inspection for Mark-LIV."""
import platform,shutil
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def drive_space_alert(parameters=None,**kwargs):
 p=parameters or {}; threshold=max(1,min(float(p.get("threshold_gb",10)),1000)); out=[]
 for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
  root=f"{letter}:\\"
  try:
   total,used,free=shutil.disk_usage(root)
   if free/1073741824<threshold:out.append(f"{root}: {free/1073741824:.2f} GB free / {total/1073741824:.2f} GB total")
  except OSError:pass
 return "\n".join(out) or f"No drives below {threshold:g} GB free."
TOOL={"name":"drive_space_alert","description":"Read-only Windows check for drives below a configurable free-space threshold.","parameters":{"type":"OBJECT","properties":{"threshold_gb":{"type":"NUMBER"}},"required":["threshold_gb"]},"handler":drive_space_alert}
