import unittest

from core.permissions import is_protected_process, needs_confirmation


class PermissionsTests(unittest.TestCase):
    def test_destructive_actions_require_confirmation(self):
        self.assertTrue(needs_confirmation("shutdown"))
        self.assertTrue(needs_confirmation("restart"))
        self.assertTrue(needs_confirmation("delete_file"))

    def test_safe_action_does_not_require_confirmation(self):
        self.assertFalse(needs_confirmation("screenshot"))
        self.assertFalse(needs_confirmation("type"))

    def test_admin_actions_require_admin_confirmation(self):
        self.assertTrue(needs_confirmation("run_as_admin", admin=True))
        self.assertTrue(needs_confirmation("change_firewall", admin=True))

    def test_protected_processes_are_detected(self):
        self.assertTrue(is_protected_process("lsass.exe"))
        self.assertTrue(is_protected_process("System"))
        self.assertFalse(is_protected_process("notepad.exe"))


if __name__ == "__main__":
    unittest.main()


    def test_launch_and_open_file_require_confirmation(self):
        self.assertTrue(needs_confirmation("launch"))
        self.assertTrue(needs_confirmation("open_file"))
