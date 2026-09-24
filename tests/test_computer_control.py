import unittest
from unittest.mock import patch

import actions.computer_control as computer_control


class ComputerControlTests(unittest.TestCase):
    def test_unknown_action_is_rejected(self):
        result = computer_control.handle({"action": "does_not_exist"})
        self.assertIsInstance(result, dict)
        self.assertFalse(result.get("ok", True))

    def test_invalid_click_button_is_rejected(self):
        result = computer_control.handle({"action": "click", "x": 10, "y": 10, "button": "invalid"})
        self.assertIsInstance(result, dict)
        self.assertFalse(result.get("ok", True))

    @patch("actions.computer_control.pyautogui.click")
    @patch("actions.computer_control._screen_size", return_value=(1920, 1080))
    def test_click_coordinates_are_clamped(self, _size, click):
        result = computer_control.handle({
            "action": "click",
            "x": 99999,
            "y": 99999,
            "button": "left",
        })
        click.assert_called_once_with(1919, 1079, button="left", clicks=1, interval=0.0)
        self.assertTrue(result.get("ok", False))


if __name__ == "__main__":
    unittest.main()
