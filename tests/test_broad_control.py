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

    @patch("actions.broad_control._execute", return_value="ok")
    def test_allowed_operation_reaches_executor(self, execute):
        result = broad_control.broad_control({
            "operation": "lock",
        })
        self.assertEqual(result, "ok")
        execute.assert_called_once_with("lock", "")


if __name__ == "__main__":
    unittest.main()
