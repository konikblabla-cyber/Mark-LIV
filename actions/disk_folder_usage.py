"""Folder disk usage inspection."""
from pathlib import Path

def disk_folder_usage(parameters=None, **kwargs):
    p = parameters or {}
    root = Path(str(p.get("path", "")).strip()).expanduser()
    if not str(root).strip():
        root = Path.home()
    try:
        limit = max(1, min(int(p.get("limit", 20)), 100))
    except (TypeError, ValueError):
        limit = 20
    if not root.exists() or not root.is_dir():
        return "Folder not found."

    rows = []
    try:
        children = list(root.iterdir())
    except OSError as e:
        return f"Cannot read folder: {e}"

    for child in children:
        if not child.is_dir():
            continue
        total = 0
        try:
            for f in child.rglob("*"):
                if f.is_file():
                    try:
                        total += f.stat().st_size
                    except OSError:
                        pass
        except OSError:
            pass
        rows.append((total, str(child)))

    rows.sort(reverse=True)
    return "\n".join(
        f"{size / 1073741824:.2f} GB\t{path}" for size, path in rows[:limit]
    ) or "No subfolders."

TOOL = {
    "name": "disk_folder_usage",
    "description": "Read-only folder usage report showing which immediate subfolders consume the most disk space.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "path": {"type": "STRING"},
            "limit": {"type": "INTEGER"},
        },
        "required": ["path"],
    },
    "handler": disk_folder_usage,
}
