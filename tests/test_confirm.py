import unittest
from unittest.mock import patch

import core.confirm as confirm


class ConfirmTests(unittest.TestCase):
    def test_request_without_ui_does_not_execute(self):
        old_show = confirm._show_cb
        confirm._show_cb = None
        ran = []
        try:
            result = confirm.request("test", "Test", "detail", lambda: ran.append(True))
            self.assertIn("interface is not available", result)
            self.assertEqual(ran, [])
        finally:
            confirm._show_cb = old_show


if __name__ == "__main__":
    unittest.main()
