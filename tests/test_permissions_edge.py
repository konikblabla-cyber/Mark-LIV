import unittest

from core.permissions import is_protected_process, needs_confirmation


class PermissionEdgeTests(unittest.TestCase):
    def test_process_matching_is_case_insensitive(self):
        self.assertTrue(is_protected_process("LSASS.EXE"))
        self.assertTrue(is_protected_process("SYSTEM"))

    def test_unknown_process_is_not_protected(self):
        self.assertFalse(is_protected_process(""))
        self.assertFalse(is_protected_process("example-app.exe"))

    def test_confirmation_is_false_for_unknown_safe_action(self):
        self.assertFalse(needs_confirmation("read_screen"))
        self.assertFalse(needs_confirmation("get_volume"))


    def test_admin_flag_requires_confirmation_for_any_action(self):
        self.assertTrue(needs_confirmation("screenshot", admin=True))

    def test_admin_sensitive_actions_require_confirmation(self):
        self.assertTrue(needs_confirmation("format_drive"))
        self.assertTrue(needs_confirmation("change_security_setting"))


if __name__ == "__main__":
    unittest.main()
