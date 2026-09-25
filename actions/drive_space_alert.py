"""Low-disk-space inspection."""
import shutil

def drive_space_alert(parameters=None, **kwargs):
    p = parameters or {}
    try:
        threshold = max(1.0, min(float(p.get("threshold_gb", 10)), 1000.0))
    except (TypeError, ValueError):
        threshold = 10.0
    out = []
    roots = [f"{letter}:\" for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    roots.append("/")
    seen = set()
    for root in roots:
        if root in seen:
            continue
        seen.add(root)
        try:
            total, used, free = shutil.disk_usage(root)
            if free / 1073741824 < threshold:
                out.append(f"{root}: {free / 1073741824:.2f} GB free / {total / 1073741824:.2f} GB total")
        except OSError:
            pass
    return "\n".join(out) or f"No drives below {threshold:g} GB free."

TOOL = {"name":"drive_space_alert","description":"Read-only check for filesystems below a configurable free-space threshold.","parameters":{"type":"OBJECT","properties":{"threshold_gb":{"type":"NUMBER"}},"required":["threshold_gb"]},"handler":drive_space_alert}
