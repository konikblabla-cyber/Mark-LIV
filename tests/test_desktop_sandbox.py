import unittest

from actions.desktop import _validate_generated_code


class DesktopSandboxTests(unittest.TestCase):
    def test_imports_are_rejected(self):
        ok, reason = _validate_generated_code("import os")
        self.assertFalse(ok)
        self.assertIn("Imports", reason)

    def test_escape_hatches_are_rejected(self):
        for code in ("open('x')", "eval('1+1')", "__import__('os')"):
            with self.subTest(code=code):
                ok, _ = _validate_generated_code(code)
                self.assertFalse(ok)

    def test_normal_code_is_allowed(self):
        ok, reason = _validate_generated_code("print(len([1, 2, 3]))")
        self.assertTrue(ok, reason)


    def test_dangerous_attribute_escape_is_rejected(self):
        for code in ("x.__subclasses__()", "x.__globals__"):
            with self.subTest(code=code):
                ok, _ = _validate_generated_code(code)
                self.assertFalse(ok)

if __name__ == "__main__":
    unittest.main()
