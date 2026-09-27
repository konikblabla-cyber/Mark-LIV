import unittest
from unittest.mock import patch

from core.action_loader import ActionRecord, ActionRegistry


class ActionLoaderTests(unittest.TestCase):
    def test_empty_registry_is_safe(self):
        registry = ActionRegistry({}, lambda _message: None)
        self.assertEqual(registry.names(), set())
        self.assertFalse(registry.has("missing"))
        self.assertEqual(registry.scheduling("missing"), None)

    def test_invalid_parameter_schema_is_rejected(self):
        from types import SimpleNamespace
        from core.action_loader import _validate
        module = SimpleNamespace(TOOL={
            "name": "bad_schema", "description": "test",
            "parameters": {"type": "STRING"}, "handler": lambda parameters=None: None,
        })
        records = _validate(module, "bad_schema.py")
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertFalse(record.valid)
        self.assertIn("parameters", record.error)

    def test_reserved_context_is_not_exposed_as_tool(self):
        registry = ActionRegistry({}, lambda _message: None)
        self.assertFalse(registry.has("player"))
        self.assertFalse(registry.has("speak"))
        self.assertFalse(registry.has("response"))

    def test_read_level_blocks_unmanaged_action(self):
        called = []
        handler = lambda parameters=None: called.append(True) or "executed"
        record = ActionRecord(
            name="windows_window_move_resize",
            description="test",
            handler=handler,
            valid=True,
        )
        registry = ActionRegistry({record.name: record}, lambda _message: None)
        with patch("core.permissions.get_control_level", return_value="READ"):
            result = registry.run(record.name, {"contains": "Notepad"})
        self.assertIn("Permission denied", result)
        self.assertEqual(called, [])

    def test_confirmation_wraps_unmanaged_action(self):
        called = []
        handler = lambda parameters=None: called.append(True) or "executed"
        record = ActionRecord(
            name="shutdown",
            description="test",
            handler=handler,
            valid=True,
        )
        registry = ActionRegistry({record.name: record}, lambda _message: None)
        with patch("core.permissions.get_control_level", return_value="NORMAL"),              patch("core.confirm.pending_title", return_value=""),              patch("core.confirm.request", return_value="[CONFIRMATION_PENDING]") as request:
            result = registry.run(record.name, {})
        self.assertEqual(result, "[CONFIRMATION_PENDING]")
        self.assertEqual(called, [])
        request.assert_called_once()

    def test_permission_managed_handler_is_not_double_gated(self):
        called = []
        handler = lambda parameters=None: called.append(True) or "executed"
        record = ActionRecord(
            name="computer_control",
            description="test",
            handler=handler,
            valid=True,
        )
        registry = ActionRegistry({record.name: record}, lambda _message: None)
        with patch("core.confirm.request") as request,              patch("core.permissions.permission_decision") as decision:
            result = registry.run(record.name, {"action": "screenshot"})
        self.assertEqual(result, "executed")
        self.assertEqual(called, [True])
        decision.assert_not_called()
        request.assert_not_called()


if __name__ == "__main__":
    unittest.main()
