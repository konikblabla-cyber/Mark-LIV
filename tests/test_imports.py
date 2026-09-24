import importlib
import unittest


MODULES = (
    "core.action_loader",
    "core.confirm",
    "core.llm_client",
    "core.permissions",
    "memory.memory_manager",
    "actions.computer_control",
    "actions.broad_control",
    "actions.close_all_apps",
    "actions.computer_settings",
    "actions.desktop",
)


class ImportSmokeTests(unittest.TestCase):
    def test_core_and_action_modules_import(self):
        for module_name in MODULES:
            with self.subTest(module=module_name):
                self.assertIsNotNone(importlib.import_module(module_name))


if __name__ == "__main__":
    unittest.main()
