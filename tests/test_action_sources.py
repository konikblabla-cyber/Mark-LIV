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
