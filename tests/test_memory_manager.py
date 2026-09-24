import unittest

from memory.memory_manager import _truncate_value, search_memory


class MemoryManagerTests(unittest.TestCase):
    def test_truncate_value_has_a_hard_limit(self):
        value = "x" * 1000
        result = _truncate_value(value)
        self.assertLessEqual(len(result), 381)
        self.assertTrue(result.endswith("…"))

    def test_search_memory_handles_empty_store(self):
        result = search_memory("definitely-not-stored")
        self.assertIn("Nothing stored", result)


if __name__ == "__main__":
    unittest.main()
