import json

from core.task_manager import TaskManager


def test_task_plan_persists_and_recovers(tmp_path):
    path = tmp_path / "tasks.json"
    manager = TaskManager(str(path))
    task_id = manager.create("test goal")
    manager.set_plan(task_id, [
        {"action": "open_app", "parameters": {"app": "Opera GX"}, "verify": "opened"},
        {"action": "verify_state", "parameters": {}, "verify": "ready"},
    ], max_retries=2)
    manager.mark_step(task_id, 0, "completed", "opened")
    assert manager.retry_step(task_id) is True

    # Simulate a fresh process by constructing a new manager from the same file.
    restored = TaskManager(str(path))
    task = restored.get(task_id)
    assert task["steps"][0]["status"] == "completed"
    assert task["current_step"] == 0
    assert task["next_step"] == 1
    assert task["retry_count"] == 1
    assert restored.recoverable() and restored.recoverable()[0]["id"] == task_id
    assert restored.get_plan(task_id)[0]["action"] == "open_app"
    assert restored.get_plan(task_id)[0]["parameters"]["app"] == "Opera GX"


def test_retry_is_bounded(tmp_path):
    manager = TaskManager(str(tmp_path / "tasks.json"))
    task_id = manager.create("retry goal")
    manager.set_plan(task_id, ["step"], max_retries=1)
    assert manager.retry_step(task_id) is True
    assert manager.retry_step(task_id) is False


def test_plan_is_bounded(tmp_path):
    manager = TaskManager(str(tmp_path / "tasks.json"))
    task_id = manager.create("bounded")
    manager.set_plan(task_id, [f"step-{i}" for i in range(150)], max_retries=99)
    task = manager.get(task_id)
    assert len(task["steps"]) == 100
    assert task["max_retries"] == 5
