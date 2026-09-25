"""High-level autonomous task runner exposed to JARVIS."""
from core.autonomy import AutonomyEngine
from core.task_manager import TaskManager

def autonomous_task(parameters, player=None, speak=None, response=None,
                    session_memory=None, action_registry=None, **kwargs):
    goal = str(parameters.get("goal") or "").strip()
    if not goal:
        return "Missing goal."

    registry = action_registry
    if registry is None:
        return "Autonomy is unavailable: action registry was not provided."

    ctx = {
        "player": player,
        "speak": speak,
        "response": response,
        "session_memory": session_memory,
        "action_registry": registry,
    }
    engine = AutonomyEngine(registry, ctx=ctx, task_manager=TaskManager())
    return engine.run(goal)

TOOL = {
    "name": "autonomous_task",
    "description": (
        "High-level JARVIS autonomy. Give it a concrete goal, not a single "
        "button click. It can inspect the PC, plan multiple actions, execute "
        "them through the normal safety/confirmation layer, recover from "
        "failures, and replan. Use this for requests such as 'audit my disk "
        "and clean up unnecessary files' or multi-step PC management tasks."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "goal": {
                "type": "STRING",
                "description": "The complete user goal in natural language."
            }
        },
        "required": ["goal"]
    },
    "handler": autonomous_task,
}
