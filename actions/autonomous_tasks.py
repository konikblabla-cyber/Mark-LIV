"""Inspect and resume persisted autonomous JARVIS tasks."""
from core.task_manager import TaskManager

def _mgr():
    return TaskManager()

def autonomous_tasks(parameters, **kwargs):
    tasks = _mgr().recoverable()
    if not tasks:
        return {"ok": True, "tasks": [], "message": "No recoverable autonomous tasks."}
    return {"ok": True, "tasks": tasks}

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
