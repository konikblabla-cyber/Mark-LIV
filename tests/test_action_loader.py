import unittest

from core.action_loader import ActionRegistry


class ActionLoaderTests(unittest.TestCase):
    def test_empty_registry_is_safe(self):
        registry = ActionRegistry()
        self.assertEqual(registry.names(), [])
        self.assertFalse(registry.has("missing"))

    def test_reserved_context_is_not_exposed_as_tool(self):
        registry = ActionRegistry()
        self.assertFalse(registry.has("player"))
        self.assertFalse(registry.has("speak"))
        self.assertFalse(registry.has("response"))


if __name__ == "__main__":
    unittest.main()
