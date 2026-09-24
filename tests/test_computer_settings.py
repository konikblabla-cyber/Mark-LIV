import unittest
from unittest.mock import patch

import actions.computer_settings as settings


class ComputerSettingsTests(unittest.TestCase):
    @patch("actions.computer_settings.volume_set")
    @patch("actions.computer_settings.volume_get", return_value=35)
    def test_volume_up_registers_undo(self, get_volume, set_volume):
        with patch("actions.computer_settings.push_undo") as push:
            result = settings._apply_volume_delta(10)
        self.assertIn("Volume", result)
        set_volume.assert_called_once_with(45)
        push.assert_called_once()

    @patch("actions.computer_settings.brightness_set")
    @patch("actions.computer_settings.brightness_get", return_value=60)
    def test_brightness_set_clamps_value(self, get_brightness, set_brightness):
        settings.brightness_set(150)
        set_brightness.assert_called_once_with(100)


if __name__ == "__main__":
    unittest.main()
