"""Central action discovery and dispatch with a final permission boundary."""
from __future__ import annotations

import importlib.util
import inspect
import re
import sys
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

_NAME_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]{0,63}$")
_DEFAULT_PARAMS = {"type": "OBJECT", "properties": {}}
_CTX_KEYS = ("player", "speak", "response", "session_memory", "action_registry")
_BEHAVIORS = ("BLOCKING", "NON_BLOCKING")
_SCHEDULING = ("WHEN_IDLE", "SILENT", "INTERRUPT")

# These handlers already implement their own parameter-aware permission gate.
_PERMISSION_MANAGED = {"computer_control", "broad_control", "close_all_apps", "system_control", "file_control", "browser_control", "desktop_control", "computer_settings"}


def _opt_upper(value, allowed: tuple[str, ...]) -> Optional[str]:
    v = str(value or "").strip().upper()
    return v if v in allowed else None


@dataclass
class ActionRecord:
    name: str
    description: str = ""
    parameters: dict = field(default_factory=lambda: dict(_DEFAULT_PARAMS))
    handler: Optional[Callable] = None
    file: str = ""
    valid: bool = False
    error: str = ""
    behavior: Optional[str] = None
    scheduling: Optional[str] = None


class ActionRegistry:
    def __init__(self, actions: dict[str, ActionRecord], logger: Callable[[str], None]):
        self._actions = actions
        self._all_records: list[ActionRecord] = []
        self._logger = logger

    def get_tool_declarations(self) -> list[dict]:
        try:
            from core.preference_learner import top_actions
            weights = dict(top_actions(100))
        except Exception:
            weights = {}
        records = sorted(
            self._actions.values(),
            key=lambda rec: (-int(weights.get(rec.name.lower(), 0)), rec.name.lower()),
        )
        out = []
        for rec in records:
            decl = {"name": rec.name, "description": rec.description,
                    "parameters": rec.parameters}
            if rec.behavior:
                decl["behavior"] = rec.behavior
            out.append(decl)
        return out

    def has(self, name: str) -> bool:
        return name in self._actions

    def scheduling(self, name: str) -> Optional[str]:
        rec = self._actions.get(name)
        return rec.scheduling if rec else None

    def names(self) -> set[str]:
        return set(self._actions.keys())

    def run(self, name: str, parameters: dict, ctx: dict | None = None) -> str:
        rec = self._actions.get(name)
        if rec is None or not rec.valid:
            return f"Action '{name}' is not available."

        context = ctx or {}
        try:
            if name not in _PERMISSION_MANAGED:
                from core.permissions import permission_decision
                from core import confirm

                decision, reason = permission_decision(name, parameters or {})
                if decision == "deny":
                    return f"Permission denied: {reason}"
                if decision == "confirm":
                    if confirm.pending_title():
                        return "There is already a confirmation waiting on screen. Ask the user to answer it first."

                    def _confirmed_run() -> str:
                        return _call_handler(rec.handler, parameters, context) or "Done."

                    return confirm.request(
                        key=f"action-{name}",
                        title=f"Allow JARVIS to run: {name}?",
                        detail=f"{reason}. JARVIS will wait for your confirmation before executing it.",
                        run=_confirmed_run,
                    )

            result = _call_handler(rec.handler, parameters, context) or "Done."
            try:
                from core.preference_learner import record_action
                record_action(name)
            except Exception:
                pass
            return result
        except Exception as e:
            message = f"Action '{name}' crashed during run(): {e}"
            self._logger(message)
            try:
                from core.status_center import record
                record("action_error", message, level="error")
            except Exception:
                pass
            try:
                from actions.jarvis_self_repair import jarvis_self_repair
                repair = jarvis_self_repair({})
                self._logger("[ActionLoader] bounded self-repair: " + str(repair)[:300])
            except Exception as repair_error:
                self._logger(f"[ActionLoader] self-repair unavailable: {repair_error}")
            traceback.print_exc()
            return f"Tool '{name}' failed: {e}"


def _call_handler(fn: Callable, parameters: dict, ctx: dict) -> str:
    sig = inspect.signature(fn)
    has_var_kw = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
    kwargs = {}
    for key in _CTX_KEYS:
        if has_var_kw or key in sig.parameters:
            kwargs[key] = ctx.get(key)
    return fn(parameters=parameters, **kwargs)


def _validate_tool(tool, filename: str, fallback_name: str) -> ActionRecord:
    if not isinstance(tool, dict):
        return ActionRecord(name=fallback_name, file=filename,
                            error="TOOL entry must be a dict.")

    name = tool.get("name")
    if not isinstance(name, str) or not _NAME_RE.match(name):
        return ActionRecord(name=str(name or fallback_name), file=filename,
                            error="TOOL['name'] missing or not a valid identifier.")

    description = tool.get("description")
    if not isinstance(description, str) or not description.strip():
        return ActionRecord(name=name, file=filename,
                            error="TOOL['description'] missing or empty.")

    parameters = tool.get("parameters", _DEFAULT_PARAMS)
    if not isinstance(parameters, dict) or parameters.get("type") != "OBJECT":
        return ActionRecord(name=name, file=filename,
                            error='TOOL parameters must be an OBJECT schema.')

    handler = tool.get("handler")
    if not callable(handler):
        return ActionRecord(name=name, file=filename,
                            error="TOOL handler missing or not callable.")

    return ActionRecord(name=name, description=description.strip(), parameters=parameters,
                        handler=handler, file=filename, valid=True,
                        behavior=_opt_upper(tool.get("behavior"), _BEHAVIORS),
                        scheduling=_opt_upper(tool.get("scheduling"), _SCHEDULING))


def _validate(module, filename: str) -> list[ActionRecord]:
    tool = getattr(module, "TOOL", None)
    if tool is None:
        return []
    entries = tool if isinstance(tool, list) else [tool]
    return [_validate_tool(entry, filename, Path(filename).stem) for entry in entries]


def discover_actions(actions_dir: Path, reserved_names: set[str] | None = None,
                     logger: Callable[[str], None] = print) -> ActionRegistry:
    reserved = reserved_names or set()
    actions_dir.mkdir(parents=True, exist_ok=True)
    valid: dict[str, ActionRecord] = {}
    all_records: list[ActionRecord] = []

    files = sorted(actions_dir.glob("*.py"), key=lambda p: p.name)
    for path in files:
        if path.name.startswith("_"):
            continue
        try:
            module_name = f"actions.{path.stem}"
            module = sys.modules.get(module_name)
            if module is None:
                spec = importlib.util.spec_from_file_location(module_name, path)
                if spec is None or spec.loader is None:
                    raise ImportError("could not build import spec")
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                try:
                    spec.loader.exec_module(module)
                except Exception:
                    sys.modules.pop(module_name, None)
                    raise

            if getattr(module, "TOOL", None) is None:
                continue

            records = _validate(module, path.name)
            for rec in records:
                if rec.valid and rec.name in reserved:
                    rec = ActionRecord(name=rec.name, file=path.name,
                                       error=f"Name '{rec.name}' collides with a reserved core tool — rejected.")
                elif rec.valid and rec.name in valid:
                    other = valid[rec.name].file
                    rec = ActionRecord(name=rec.name, file=path.name,
                                       error=f"Name '{rec.name}' already used by action '{other}' — rejected.")

                all_records.append(rec)
                if rec.valid:
                    valid[rec.name] = rec
                    logger(f"Action loaded: {rec.name} ({path.name})")
                else:
                    logger(f"Action rejected: {path.name} — {rec.error}")

        except Exception as e:
            rec = ActionRecord(name=path.stem, file=path.name,
                               error=f"Failed to load: {e}")
            all_records.append(rec)
            traceback.print_exc()
            logger(f"Action rejected: {path.name} — {rec.error}")

    registry = ActionRegistry(valid, logger)
    registry._all_records = all_records
    logger(f"Action discovery complete: {len(valid)} active.")
    return registry
