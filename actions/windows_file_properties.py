"""Read-only Windows file metadata."""
import os, platform

def windows_file_properties(parameters=None, **kwargs):
    if platform.system() != "Windows":
        return "Windows-only action."
    p = str((parameters or {}).get("path") or "").strip()
    if not p:
        return "Missing path."
    if not os.path.exists(p):
        return f"Path does not exist: {p}"
    s = os.stat(p)
    kind = "directory" if os.path.isdir(p) else "file"
    return f"Path: {p}\nType: {kind}\nSize: {s.st_size} bytes\nCreated: {s.st_ctime}\nModified: {s.st_mtime}"

TOOL={"name":"windows_file_properties","description":"Read-only Windows file or folder basic metadata.","parameters":{"type":"OBJECT","properties":{"path":{"type":"STRING"}},"required":["path"]},"handler":windows_file_properties}
