"""Open an existing Windows folder."""
import os
import platform

def windows_folder_open(parameters=None, **kwargs):
    if platform.system() != "Windows":
        return "windows_folder_open is Windows-only."
    path = str((parameters or {}).get("path", "")).strip()
    if not path or not os.path.isdir(path):
        return f"Folder not found: {path}"
    try:
        os.startfile(path)
        return f"Opened folder: {path}"
    except OSError as e:
        return f"Failed to open folder: {e}"

TOOL = {
    "name": "windows_folder_open",
    "description": "Open an existing Windows folder directly in File Explorer.",
    "parameters": {
        "type": "OBJECT",
        "properties": {"path": {"type": "STRING"}},
        "required": ["path"],
    },
    "handler": windows_folder_open,
}
