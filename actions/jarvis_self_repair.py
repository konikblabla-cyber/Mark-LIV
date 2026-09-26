"""Cheap local JARVIS health, repair and protection checks.

No Gemini call is made here. Repairs are limited to reversible runtime setup.
"""
from __future__ import annotations

import json
import os
import platform
import shutil
import tempfile
from pathlib import Path

import psutil

PROTECTED = {
    "System", "Registry", "smss.exe", "csrss.exe", "wininit.exe",
    "winlogon.exe", "services.exe", "lsass.exe", "svchost.exe",
    "dwm.exe", "explorer.exe",
}


def _runtime_root() -> Path:
    return Path(os.environ.get("PROGRAMDATA", ".")) / "Mark-LIV"


def _check_core():
    checks = []
    modules = (
        "core.confirm",
        "core.autonomy",
        "core.autonomy_monitor",
        "memory.memory_manager",
    )
    for name in modules:
        try:
            __import__(name)
            checks.append((name, True, "import OK"))
        except Exception as exc:
            checks.append((name, False, str(exc)[:180]))
    return checks


def _safe_write_json(path: Path, data) -> None:
    """Atomically replace a small runtime JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass


def _backup_corrupt(path: Path) -> Path | None:
    """Keep a recoverable copy before repairing a corrupt runtime file."""
    try:
        backup = path.with_name(f"{path.stem}.corrupt-backup{path.suffix}")
        if backup.exists():
            backup = path.with_name(
                f"{path.stem}.corrupt-backup-{os.getpid()}{path.suffix}"
            )
        shutil.copy2(path, backup)
        return backup
    except OSError:
        return None


def jarvis_self_repair(parameters=None, **kwargs):
    """Run local diagnostics and apply only safe, reversible runtime repairs."""
    if platform.system() != "Windows":
        return "JARVIS self-repair is currently Windows-only."

    results = []
    root = _runtime_root()

    try:
        root.mkdir(parents=True, exist_ok=True)
        results.append("runtime directory OK")
    except OSError as exc:
        return f"Self-repair stopped: cannot prepare runtime directory: {exc}"

    task_file = root / "jarvis_tasks.json"
    try:
        if task_file.exists() and not task_file.is_file():
            return "Self-repair stopped: task storage path is not a file."
        if not task_file.exists():
            _safe_write_json(task_file, {})
            results.append("recreated missing task storage")
        else:
            try:
                data = json.loads(task_file.read_text(encoding="utf-8"))
                if not isinstance(data, dict):
                    raise ValueError("task storage root is not an object")
                results.append("task storage OK")
            except Exception as exc:
                backup = _backup_corrupt(task_file)
                _safe_write_json(task_file, {})
                if backup:
                    results.append(
                        f"replaced corrupt task storage (backup: {backup.name})"
                    )
                else:
                    results.append(
                        f"replaced corrupt task storage (backup failed: {exc.__class__.__name__})"
                    )
    except OSError as exc:
        results.append(f"task storage check failed: {exc}")

    for name, ok, detail in _check_core():
        results.append(f"{name}: {'OK' if ok else 'FAIL'} ({detail})")

    message = "JARVIS self-repair: " + "; ".join(results)
    try:
        from core.status_center import record
        level = "warning" if any(
            "FAIL" in item or "failed" in item for item in results
        ) else "info"
        record("repair", message, level=level)
    except Exception:
        pass
    return message


def jarvis_protection_fingerprint(parameters=None, **kwargs):
    """Return a cheap stable snapshot of unusually heavy non-protected processes."""
    findings = []
    protected = {x.lower() for x in PROTECTED}
    try:
        current = psutil.Process()
        current_pid = current.pid
    except Exception:
        current_pid = -1
    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            info = proc.info
            name = info.get("name") or "?"
            if int(info.get("pid") or 0) == current_pid:
                continue
            if name.lower() in protected:
                continue
            cpu = float(info.get("cpu_percent") or 0)
            ram = float(info.get("memory_percent") or 0)
            if cpu >= 90.0 or ram >= 15.0:
                findings.append((name.lower(), int(info.get("pid") or 0)))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return sorted(findings)[:8]


def jarvis_protection_check(parameters=None, **kwargs):
    """Detect unusual resource-heavy processes without killing or changing anything."""
    p = parameters or {}
    try:
        cpu_limit = max(80.0, min(float(p.get("cpu_limit", 90.0)), 100.0))
    except (TypeError, ValueError):
        cpu_limit = 90.0
    try:
        ram_limit = max(10.0, min(float(p.get("ram_limit", 15.0)), 100.0))
    except (TypeError, ValueError):
        ram_limit = 15.0
    findings = []
    protected = {x.lower() for x in PROTECTED}

    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            info = proc.info
            name = info.get("name") or "?"
            if name.lower() in protected:
                continue
            cpu = float(info.get("cpu_percent") or 0)
            ram = float(info.get("memory_percent") or 0)
            if cpu >= cpu_limit or ram >= ram_limit:
                findings.append(
                    f"PID {info.get('pid')}: {name} | CPU {cpu:.0f}% | RAM {ram:.1f}%"
                )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if not findings:
        return "Protection check: no unusual non-protected process load detected."
    findings = findings[:10]
    message = "Protection check: attention needed (no action taken):\n- " + "\n- ".join(findings)
    try:
        from core.status_center import record
        record("protection", message, level="warning")
    except Exception:
        pass
    return message


TOOL = [
    {
        "name": "jarvis_self_repair",
        "description": "Run cheap local JARVIS diagnostics and repair only missing/corrupt runtime state with a backup; never changes security or kills processes.",
        "parameters": {"type": "OBJECT", "properties": {}},
        "handler": jarvis_self_repair,
    },
    {
        "name": "jarvis_protection_fingerprint",
        "description": "Create a cheap stable snapshot of unusually heavy non-protected processes for anomaly detection; read-only.",
        "parameters": {"type": "OBJECT", "properties": {}},
        "handler": jarvis_protection_fingerprint,
    },
    {
        "name": "jarvis_protection_check",
        "description": "Locally detect unusually CPU/RAM-heavy non-protected processes. Read-only: never kills or changes anything.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "cpu_limit": {"type": "NUMBER"},
                "ram_limit": {"type": "NUMBER"},
            },
        },
        "handler": jarvis_protection_check,
    },
]
