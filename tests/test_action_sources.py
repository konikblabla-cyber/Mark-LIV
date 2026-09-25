import ast
from pathlib import Path
import unittest

class ActionSourceTests(unittest.TestCase):
    def test_all_action_sources_are_valid_and_declarations_have_required_keys(self):
        root = Path(__file__).resolve().parents[1] / "actions"
        failures = []
        for path in sorted(root.glob("*.py")):
            source = path.read_text(encoding="utf-8")
            try:
                tree = ast.parse(source, filename=str(path))
            except SyntaxError as exc:
                failures.append(f"{path.name}: SyntaxError {exc}")
                continue
            for node in tree.body:
                if not isinstance(node, ast.Assign):
                    continue
                if not any(isinstance(t, ast.Name) and t.id == "TOOL" for t in node.targets):
                    continue
                if not isinstance(node.value, ast.Dict):
                    failures.append(f"{path.name}: TOOL is not a dict")
                    continue
                keys = [k.value for k in node.value.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)]
                for required in ("name", "description", "parameters", "handler"):
                    if required not in keys:
                        failures.append(f"{path.name}: TOOL missing '{required}'")
        self.assertFalse(failures, "\n".join(failures))

    def test_tool_names_are_unique(self):
        root = Path(__file__).resolve().parents[1] / "actions"
        seen = {}
        duplicates = []
        for path in sorted(root.glob("*.py")):
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except SyntaxError:
                continue
            for node in tree.body:
                if not isinstance(node, ast.Assign) or not any(isinstance(t, ast.Name) and t.id == "TOOL" for t in node.targets):
                    continue
                if not isinstance(node.value, ast.Dict):
                    continue
                pairs = zip(node.value.keys, node.value.values)
                for key, value in pairs:
                    if isinstance(key, ast.Constant) and key.value == "name" and isinstance(value, ast.Constant) and isinstance(value.value, str):
                        name = value.value
                        if name in seen:
                            duplicates.append(f"{name}: {seen[name]} + {path.name}")
                        else:
                            seen[name] = path.name
        self.assertFalse(duplicates, "Duplicate TOOL names:\n" + "\n".join(duplicates))
