import unittest
from unittest.mock import patch

import actions.broad_control as broad_control


class BroadControlTests(unittest.TestCase):
    def test_unknown_operation_is_rejected(self):
        result = broad_control.broad_control({"operation": "delete_everything"})
        self.assertIn("supported operation", result)

    def test_missing_target_is_rejected(self):
        result = broad_control.broad_control({"operation": "launch"})
        self.assertEqual(result, "A target is required.")

    @patch("actions.broad_control._execute", return_value="JARVIS is running without administrator privileges.")
    @patch("actions.broad_control.is_admin", return_value=False)
    def test_admin_status_reports_non_elevated(self, is_admin, execute):
        result = broad_control.broad_control({"operation": "admin_status"})
        self.assertIn("without administrator", result)
        execute.assert_called_once_with("admin_status")

    @patch("actions.broad_control._execute", return_value="Administrator command requested.")
    @patch("actions.broad_control.needs_confirmation", return_value=False)
    @patch("actions.broad_control.is_admin", return_value=False)
    @patch("actions.broad_control.command_needs_admin", return_value=True)
    def test_admin_hint_requests_elevation(self, admin_hint, is_admin, needs, execute):
        result = broad_control.broad_control({"operation": "run_command", "target": "sc stop TestService"})
        self.assertIn("Administrator command requested", result)
        execute.assert_called_once_with("run_as_admin", "sc stop TestService")

    @patch("actions.broad_control._execute", return_value="Command exit=5:\nAccess is denied.")
    @patch("actions.broad_control.needs_confirmation", side_effect=lambda action, admin=False: admin)
    @patch("actions.broad_control.is_admin", return_value=False)
    @patch("actions.broad_control.is_admin_failure", return_value=True)
    @patch("actions.broad_control.confirm.request", side_effect=lambda **kwargs: kwargs["run"]())
    def test_access_denied_can_retry_as_admin(self, admin_failure, is_admin, needs, execute, confirm_request):
        result = broad_control.broad_control({"operation": "run_command", "target": "some-command"})
        self.assertIn("Access is denied", result)
        self.assertTrue(execute.called)

    @patch("actions.broad_control._execute", return_value="ok")
    def test_allowed_operation_reaches_executor(self, execute):
        result = broad_control.broad_control({
            "operation": "lock",
        })
        self.assertEqual(result, "ok")
        execute.assert_called_once_with("lock", "")

    @patch("actions.broad_control.subprocess.Popen")
    @patch("actions.broad_control.shlex.split", return_value=["notepad.exe"])
    @patch("actions.broad_control._OS", "Windows")
    @patch("actions.broad_control.needs_confirmation", return_value=False)
    def test_launch_does_not_use_shell(self, needs, split, popen):
        result = broad_control.broad_control({"operation": "launch", "target": "notepad.exe"})
        self.assertIn("Launched", result)
        self.assertFalse(popen.call_args.kwargs.get("shell", False))

if __name__ == "__main__":
    unittest.main()
