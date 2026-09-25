import ast
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TARGETS=[
"actions/computer_control.py",
"actions/file_controller.py",
"actions/network_diagnostics.py",
"actions/system_control.py",
"actions/windows_notification_action.py",
]
out=[]
for rel in TARGETS:
    path=ROOT/rel
    source=path.read_text(encoding="utf-8")
    try:
        tree=ast.parse(source,filename=str(path))
    except SyntaxError as e:
        out.append(f"{rel}: SyntaxError line {e.lineno}, col {e.offset}: {e.msg}")
        continue
    found=False
    for node in tree.body:
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="TOOL" for t in node.targets):
            found=True
            if not isinstance(node.value,ast.Dict):
                out.append(f"{rel}: TOOL is not a dict")
                continue
            keys=[k.value for k in node.value.keys if isinstance(k,ast.Constant) and isinstance(k.value,str)]
            missing=[k for k in ("name","description","parameters","handler") if k not in keys]
            if missing: out.append(f"{rel}: missing TOOL keys: {', '.join(missing)}")
    if not found:
        out.append(f"{rel}: no module-level TOOL assignment")
report="\n".join(out) if out else "ALL_TARGETS_VALID"
(ROOT/"tests"/"action_validation_report.txt").write_text(report+"\n",encoding="utf-8")
print(report)
