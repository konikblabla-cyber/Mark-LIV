import ast
import os
from pathlib import Path
import unittest

class ActionSourceTests(unittest.TestCase):
    def test_all_action_sources_are_valid_and_declarations_have_required_keys(self):
        root = Path(__file__).resolve().parents[1] / "actions"
        paths = sorted(root.glob("*.py"))
        start = int(os.environ.get("ACTION_START", "0"))
        end = int(os.environ.get("ACTION_END", str(len(paths))))
        failures = []
        for index, path in enumerate(paths):
            if not (start <= index < end):
                continue
            source = path.read_text(encoding="utf-8")
            try:
                tree = ast.parse(source, filename=str(path))
            except SyntaxError as exc:
                failures.append(f"{index}:{path.name}: SyntaxError {exc}")
                continue
            for node in tree.body:
                if not isinstance(node, ast.Assign):
                    continue
                if not any(isinstance(t, ast.Name) and t.id == "TOOL" for t in node.targets):
                    continue
                if not isinstance(node.value, ast.Dict):
                    failures.append(f"{index}:{path.name}: TOOL is not a dict")
                    continue
                keys = [k.value for k in node.value.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)]
                for required in ("name", "description", "parameters", "handler"):
                    if required not in keys:
                        failures.append(f"{index}:{path.name}: TOOL missing '{required}'")
        report = "\n".join(failures) if failures else "ALL_ACTION_SOURCES_VALID"
        (root.parent / "tests" / "action_validation_report.txt").write_text(report + "\n", encoding="utf-8")
        self.assertFalse(failures, report)
