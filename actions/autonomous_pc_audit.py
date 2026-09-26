"""High-level autonomous PC audit for Mark-LIV.
This is a decision layer: it gathers evidence, filters noise, and produces
actionable recommendations instead of dumping raw telemetry.
"""
from __future__ import annotations
import os
import platform
import shutil
import time
from pathlib import Path
import subprocess
import psutil

PROTECTED = {"System", "Registry", "smss.exe", "csrss.exe", "wininit.exe",
             "winlogon.exe", "services.exe", "lsass.exe", "svchost.exe",
             "dwm.exe", "explorer.exe"}

def _top_processes(limit=8):
    rows=[]
    for p in psutil.process_iter(["pid","name","memory_percent","cpu_percent"]):
        try:
            info=p.info
            name=info.get("name") or "?"
            if name in PROTECTED: continue
            rows.append((float(info.get("memory_percent") or 0), float(info.get("cpu_percent") or 0),
                         int(info.get("pid") or 0), name))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return sorted(rows, reverse=True)[:limit]

def autonomous_pc_audit(parameters=None, **kwargs):
    p=parameters or {}
    threshold=max(50,min(int(p.get("disk_threshold",80)),99))
    disks=[]
    for part in psutil.disk_partitions(all=False):
        try:
            u=psutil.disk_usage(part.mountpoint)
            disks.append((part.mountpoint,u.percent,u.free,u.total))
        except (OSError,PermissionError):
            pass
    vm=psutil.virtual_memory()
    boot=time.time()-psutil.boot_time()
    rec=[]
    for mount,pct,free,total in disks:
        if pct>=threshold:
            rec.append(f"HIGH: {mount} ma {pct:.1f}% zajętości — uruchom analizę storage_cleanup_advisor.")
    if vm.percent>=85:
        rec.append(f"HIGH: RAM {vm.percent:.1f}% — sprawdź procesy obciążające pamięć.")
    if not rec:
        rec.append("Brak krytycznych problemów wykrytych w podstawowym audycie.")
    lines=[
        "JARVIS AUTONOMOUS PC AUDIT",
        f"System: {platform.platform()}",
        f"Uptime: {boot/86400:.1f} dni",
        f"RAM: {vm.percent:.1f}% ({vm.available/1073741824:.1f} GB dostępne)",
        "Dyski:"
    ]
    lines += [f"- {m}: {pct:.1f}% zajęte, {free/1073741824:.1f} GB wolne" for m,pct,free,total in disks]
    lines.append("Priorytety:")
    lines += [f"- {x}" for x in rec]
    lines.append("Procesy wymagające uwagi:")
    lines += [f"- PID {pid} {name}: RAM {mem:.1f}%, CPU {cpu:.1f}%" for mem,cpu,pid,name in _top_processes()]
    return "\n".join(lines)

def close_process(parameters=None, **kwargs):
    """Close a non-protected process only after the shared confirmation gate."""
    p = parameters or {}
    try:
        pid = int(p.get("pid", 0))
    except (TypeError, ValueError):
        return "Valid PID required."
    if pid <= 0:
        return "Valid PID required."
    try:
        proc = psutil.Process(pid)
        name = proc.name() or "unknown"
        if name in PROTECTED or name.lower() in {x.lower() for x in PROTECTED}:
            return f"Refused to close protected process {name} (PID {pid})."
        detail = f"JARVIS will close {name} (PID {pid}). Unsaved work in that process may be lost."
        from core import confirm
        return confirm.request(
            key=f"process:{pid}",
            title=f"Close process: {name} (PID {pid})",
            detail=detail,
            run=lambda: _terminate_process(pid),
        )
    except psutil.NoSuchProcess:
        return "That process is no longer running."
    except psutil.AccessDenied:
        return "Access denied; I will not force-close that process."


def _terminate_process(pid: int) -> str:
    try:
        proc = psutil.Process(pid)
        name = proc.name() or "unknown"
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except psutil.TimeoutExpired:
            return f"{name} did not close within 3 seconds; nothing more forceful was attempted."
        return f"Closed {name} (PID {pid})."
    except psutil.NoSuchProcess:
        return "Process already closed."
    except psutil.AccessDenied:
        return "Access denied; process was not closed."


def safe_pc_optimization(parameters=None, **kwargs):
    """Choose only low-risk maintenance relevant to the detected local state."""
    if platform.system() != "Windows":
        return "Windows-only optimization."
    results = []
    vm = psutil.virtual_memory()
    if vm.percent >= 85:
        top = _top_processes(limit=3)
        if top:
            results.append(
                "RAM is high; no process was closed. Top load: " +
                ", ".join(f"{name} PID {pid} ({mem:.1f}% RAM)" for mem, cpu, pid, name in top)
            )
        else:
            results.append("RAM is high; no safe automatic process action was available.")
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
            if usage.percent >= 90:
                results.append(
                    f"{part.mountpoint} is {usage.percent:.0f}% full; cleanup requires explicit file selection."
                )
        except (OSError, PermissionError):
            pass
    try:
        proc = subprocess.run(
            ["ipconfig", "/flushdns"],
            capture_output=True, text=True, timeout=20,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        results.append("DNS cache refreshed" if proc.returncode == 0 else "DNS refresh skipped")
    except Exception as exc:
        results.append(f"DNS refresh unavailable: {str(exc)[:120]}")
    return "Safe optimization: " + ("; ".join(results) if results else "no low-risk action was needed.")

TOOL=[
    {
        "name":"close_process",
        "description":"Close a non-protected Windows process by PID. Always uses the shared human confirmation gate; never force-kills protected/system processes.",
        "parameters":{"type":"OBJECT","properties":{"pid":{"type":"INTEGER"}},"required":["pid"]},
        "handler":close_process,
    },
    {
        "name":"autonomous_pc_audit",
        "description":"Wysokopoziomowy audyt komputera: zbiera dane, odrzuca chronione procesy i wyznacza priorytety zamiast zwracać surowy spam diagnostyczny.",
        "parameters":{"type":"OBJECT","properties":{"disk_threshold":{"type":"INTEGER","description":"Próg zajętości dysku dla rekomendacji, domyślnie 80."}}},
        "handler":autonomous_pc_audit,
    },
    {
        "name":"safe_pc_optimization",
        "description":"Wykonuje wyłącznie bezpieczne, niskiego ryzyka czynności optymalizacyjne komputera. Nie usuwa plików, nie zabija procesów i nie zmienia zabezpieczeń.",
        "parameters":{"type":"OBJECT","properties":{}},
        "handler":safe_pc_optimization,
    },
]
