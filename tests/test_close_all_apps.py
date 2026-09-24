import unittest
from unittest.mock import patch

import actions.close_all_apps as close_all_apps


class CloseAllAppsTests(unittest.TestCase):
    @patch("actions.close_all_apps._OS", "Linux")
    def test_non_windows_is_rejected(self):
        result = close_all_apps.close_all_apps()
        self.assertIn("Windows only", result)

    @patch("actions.close_all_apps.needs_confirmation", return_value=True)
    @patch("actions.close_all_apps.confirm.pending_title", return_value="")
    @patch("actions.close_all_apps.confirm.request", return_value="pending")
    def test_policy_can_gate_action(self, request, pending, needs):
        with patch("actions.close_all_apps._OS", "Windows"):
            result = close_all_apps.close_all_apps()
        self.assertEqual(result, "pending")
        request.assert_called_once()

    @patch("actions.close_all_apps.subprocess.run")
    @patch("actions.close_all_apps.needs_confirmation", return_value=False)
    def test_close_script_contains_protected_processes(self, needs, run):
        with patch("actions.close_all_apps._OS", "Windows"):
            result = close_all_apps.close_all_apps()
        self.assertIn("Requested graceful close", result)
        script = run.call_args.args[-1]
        for name in ("explorer", "dwm", "lsass", "svchost", "winlogon"):
            self.assertIn(name, script)

if __name__ == "__main__":
    unittest.main()
