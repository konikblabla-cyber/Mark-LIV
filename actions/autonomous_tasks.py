"""Inspect and resume persisted autonomous JARVIS tasks."""
from core.task_manager import TaskManager

def _mgr():
    return TaskManager()

def jarvis_self_test(parameters, action_registry=None, **kwargs):
    """Run cheap local checks; never calls Gemini and never changes user data."""
    checks = []
    try:
        count = len(action_registry.names()) if action_registry else 0
        checks.append(("action registry", count > 0, f"{count} actions"))
    except Exception as exc:
        checks.append(("action registry", False, str(exc)[:100]))
    try:
        from memory.memory_manager import load_memory
        load_memory()
        checks.append(("memory", True, "load OK"))
    except Exception as exc:
        checks.append(("memory", False, str(exc)[:100]))
    try:
        mgr = TaskManager()
        data = mgr._read()
        checks.append(("task storage", isinstance(data, dict), "read OK"))
    except Exception as exc:
        checks.append(("task storage", False, str(exc)[:100]))
    try:
        from core import confirm
        ok = all(hasattr(confirm, name) for name in ("request", "resolve", "arm_voice", "resolve_voice"))
        checks.append(("confirmation gate", ok, "API OK" if ok else "API incomplete"))
    except Exception as exc:
        checks.append(("confirmation gate", False, str(exc)[:100]))
    try:
        from core.autonomy import AutonomyEngine
        checks.append(("autonomy engine", bool(AutonomyEngine), "import OK"))
    except Exception as exc:
        checks.append(("autonomy engine", False, str(exc)[:100]))
    try:
        from actions.jarvis_self_repair import jarvis_protection_fingerprint
        snapshot = jarvis_protection_fingerprint()
        checks.append(("protection monitor", isinstance(snapshot, list), "local check OK"))
    except Exception as exc:
        checks.append(("protection monitor", False, str(exc)[:100]))
    try:
        from core.wake_word import is_installed
        installed = bool(is_installed())
        checks.append(("wake word", True, "installed" if installed else "optional/not installed"))
    except Exception as exc:
        checks.append(("wake word", True, f"optional: {str(exc)[:80]}"))
    ok = all(v for _, v, _ in checks)
    return ("JARVIS self-test: " + ("OK" if ok else "attention needed") + "\n" +
            "\n".join(f"- {name}: {'OK' if value else 'FAIL'} ({detail})"
                        for name, value, detail in checks))

def jarvis_status(parameters, action_registry=None, **kwargs):
    """Return a useful local status snapshot without spending a Gemini call."""
    from core import confirm
    import platform
    import psutil

    tasks = TaskManager().recoverable()
    count = len(action_registry.names()) if action_registry else 0
    from core.status_center import snapshot
    status_events = snapshot(6)
    pending = confirm.pending_title() or "none"
    checks = []
    for module in ("core.confirm", "core.autonomy", "core.autonomy_monitor",
                   "core.wake_word", "memory.memory_manager"):
        try:
            __import__(module)
            checks.append(True)
        except Exception:
            checks.append(False)

    health = "OK" if all(checks) else "ATTENTION"
    ram = psutil.virtual_memory()
    root = "C:\\" if platform.system() == "Windows" else "/"
    disk = psutil.disk_usage(root)
    lines = [
        f"JARVIS status: health={health}; actions={count}; "
        f"recoverable_tasks={len(tasks)}; pending_confirmation={pending}; "
        f"RAM={ram.percent:.0f}%; disk={disk.percent:.0f}%",
        f"Status center: {status_events.get('health', 'OK')}; "
        f"warnings={status_events.get('warnings', 0)}; errors={status_events.get('errors', 0)}"
    ]
    if status_events["last_issue"]:
        e = status_events["last_issue"]
        lines.append(f"Last issue: {e.get('message', '')[:180]}")
    if status_events["last_fix"]:
        e = status_events["last_fix"]
        lines.append(f"Last fix/maintenance: {e.get('message', '')[:180]}")
    if tasks:
        lines.append("Recoverable tasks:")
        for task in tasks[:5]:
            tid = str(task.get("id", ""))[:24]
            state = str(task.get("status", ""))[:24]
            goal = str(task.get("goal", ""))[:100]
            lines.append(f"- {state} {tid}: {goal}")
    if status_events["events"]:
        lines.append("Recent events:")
        lines.extend(f"- {e.get('kind')}: {e.get('message')}" for e in status_events["events"][:4])
    return "\\n".join(lines)
def autonomous_tasks(parameters, **kwargs):
    tasks = _mgr().recoverable()
    if not tasks:
        return {"ok": True, "tasks": [], "message": "No recoverable autonomous tasks."}
    return {"ok": True, "tasks": tasks}

def run_autonomous_goal(parameters, action_registry=None, player=None, speak=None,
                       response=None, session_memory=None, **kwargs):
    goal = str((parameters or {}).get("goal") or "").strip()
    if not goal or action_registry is None:
        return "Missing goal or action registry."
    from core.autonomy import AutonomyEngine
    ctx = {
        "player": player, "speak": speak, "response": response,
        "session_memory": session_memory, "action_registry": action_registry,
    }
    return AutonomyEngine(action_registry, ctx=ctx, task_manager=_mgr()).run(goal)


def resume_autonomous_task(parameters, action_registry=None, player=None, speak=None,
                           response=None, session_memory=None, **kwargs):
    task_id = str(parameters.get("task_id") or "").strip()
    if not task_id or action_registry is None:
        return "Missing task_id or action registry."
    task = _mgr().get(task_id)
    if not task:
        return "Task not found."
    if task.get("status") == "completed":
        return "Task is already completed."

    from core.autonomy import AutonomyEngine
    history = [(x.get("action", ""), x.get("result", ""))
               for x in task.get("history", [])]
    recent = history[-3:]
    # Replanning from the original goal is deliberate: persisted state is evidence,
    # not permission to blindly repeat a stale action after a restart.
    ctx = {
        "player": player, "speak": speak, "response": response,
        "session_memory": session_memory, "action_registry": action_registry,
    }
    engine = AutonomyEngine(action_registry, ctx=ctx, task_manager=_mgr(), task_id=task_id)
    plan = engine._plan(task.get("goal", ""), failure=(
"Resuming interrupted task. Inspect current state; do not blindly repeat completed steps. Recent history: " + str(recent)[-1500:]
    ))
    if not plan or not plan.steps:
        _mgr().update(task_id, status="paused")
        return "Could not safely rebuild the task plan."
    _mgr().update(task_id, status="running")
    return engine._execute_steps(plan, 0, task.get("goal", ""), history)

TOOL = [
    {
        "name": "jarvis_self_test",
        "description": "Run a cheap local health check of JARVIS core services without making changes.",
        "parameters": {"type":"OBJECT","properties":{}},
        "handler": jarvis_self_test,
    },
    {
        "name": "jarvis_status",
        "description": "Show a compact status of JARVIS actions, recoverable tasks, and pending confirmations.",
        "parameters": {"type":"OBJECT","properties":{}},
        "handler": jarvis_status,
    },
    {
        "name": "run_autonomous_goal",
        "description": "Break a larger user goal into safe steps, execute them, verify results, and replan after failures. Use for multi-step tasks rather than inventing a long manual sequence.",
        "parameters": {
            "type":"OBJECT",
            "properties":{"goal":{"type":"STRING"}},
            "required":["goal"],
        },
        "handler": run_autonomous_goal,
    },
    {
        "name": "autonomous_tasks",
        "description": "List autonomous tasks that can be recovered or resumed.",
        "parameters": {"type":"OBJECT","properties":{}},
        "handler": autonomous_tasks,
    },
    {
        "name": "resume_autonomous_task",
        "description": "Safely resume a persisted autonomous task by rebuilding its plan from current state.",
        "parameters": {
            "type":"OBJECT",
            "properties":{"task_id":{"type":"STRING"}},
            "required":["task_id"],
        },
        "handler": resume_autonomous_task,
    },
]
