import unittest
from unittest.mock import patch

from core.plugin_loader import PluginRecord, PluginRegistry


class PluginPermissionTests(unittest.TestCase):
    def _registry(self, run):
        rec = PluginRecord(
            name="test_plugin",
            description="test",
            run=run,
            valid=True,
        )
        registry = PluginRegistry({"test_plugin": rec}, lambda _message: None)
        registry._all_records = [rec]
        return registry

    def test_read_level_blocks_plugin_execution(self):
        called = []
        registry = self._registry(lambda parameters: called.append(True) or "executed")
        with patch("core.plugin_loader.get_plugin_enabled", return_value=True),              patch("core.plugin_loader.permission_decision", return_value=("deny", "READ level allows only read/inspection operations")):
            result = registry.run("test_plugin", {})
        self.assertIn("Permission denied", result)
        self.assertEqual(called, [])

    def test_consequential_plugin_waits_for_confirmation(self):
        called = []
        registry = self._registry(lambda parameters: called.append(True) or "executed")
        with patch("core.plugin_loader.get_plugin_enabled", return_value=True),              patch("core.plugin_loader.permission_decision", return_value=("confirm", "confirmation required")),              patch("core.plugin_loader.confirm_gate.pending_title", return_value=""),              patch("core.plugin_loader.confirm_gate.request", return_value="[CONFIRMATION_PENDING]") as request:
            result = registry.run("test_plugin", {})
        self.assertEqual(result, "[CONFIRMATION_PENDING]")
        self.assertEqual(called, [])
        request.assert_called_once()

    def test_normal_plugin_executes_after_permission_allows(self):
        called = []
        registry = self._registry(lambda parameters: called.append(True) or "executed")
        with patch("core.plugin_loader.get_plugin_enabled", return_value=True),              patch("core.plugin_loader.permission_decision", return_value=("allow", "normal operation")):
            result = registry.run("test_plugin", {})
        self.assertEqual(result, "executed")
        self.assertEqual(called, [True])


if __name__ == "__main__":
    unittest.main()
