"""Inspect and resume persisted autonomous JARVIS tasks."""
from core.task_manager import TaskManager

def _mgr():
    return TaskManager()

def jarvis_self_test(parameters, action_registry=None, **kwargs):
    checks = []
    try:
        checks.append(("action registry", bool(action_registry and action_registry.names())))
    except Exception:
        checks.append(("action registry", False))
    try:
        from memory.memory_manager import load_memory
        load_memory()
        checks.append(("memory", True))
    except Exception:
        checks.append(("memory", False))
    try:
        from core import confirm
        checks.append(("confirmation gate", hasattr(confirm, "request") and hasattr(confirm, "resolve")))
    except Exception:
        checks.append(("confirmation gate", False))
    try:
        from core.wake_word import is_installed
        checks.append(("wake word module", bool(is_installed())))
    except Exception:
        checks.append(("wake word module", False))
    ok = all(v for _, v in checks)
    return ("JARVIS self-test: " + ("OK" if ok else "attention needed") + "\n" +
            "\n".join(f"- {name}: {'OK' if value else 'FAIL'}" for name, value in checks))


def jarvis_status(parameters, action_registry=None, **kwargs):
    """Return a useful local status snapshot without spending a Gemini call."""
    from core import confirm
    import platform
    import psutil

    tasks = TaskManager().recoverable()
    count = len(action_registry.names()) if action_registry else 0
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
    return (
        f"JARVIS status: health={health}; actions={count}; "
        f"recoverable_tasks={len(tasks)}; pending_confirmation={pending}; "
        f"RAM={ram.percent:.0f}%; disk={disk.percent:.0f}%"
    )
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
    from core.autonomy import Plan, PlanStep

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
