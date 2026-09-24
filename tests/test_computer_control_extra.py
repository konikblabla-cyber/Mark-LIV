import unittest
from unittest.mock import patch

import actions.computer_control as computer_control


class ComputerControlExtraTests(unittest.TestCase):
    @patch("actions.computer_control._screen_size", return_value=(1920, 1080))
    @patch("actions.computer_control.pyautogui.moveTo")
    def test_move_clamps_coordinates(self, move_to, _size):
        result = computer_control.computer_control({"action": "move", "x": -10, "y": 5000})
        move_to.assert_called_once_with(0, 1079, duration=0.3)
        self.assertIn("Mouse", result)

    def test_unknown_action_is_safe(self):
        result = computer_control.computer_control({"action": "definitely_unknown"})
        self.assertIn("Unknown action", result)

    def test_user_data_does_not_crash_when_memory_is_missing(self):
        with patch.object(computer_control, "_user_profile", return_value={}):
            result = computer_control.computer_control({"action": "user_data", "field": "name"})
        self.assertIsInstance(result, str)


if __name__ == "__main__":
    unittest.main()
