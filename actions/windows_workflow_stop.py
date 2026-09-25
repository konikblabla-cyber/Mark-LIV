"""Local stop signal for bounded workflows."""
import platform,threading
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
_stop=threading.Event()
def windows_workflow_stop(parameters=None,**kwargs):
 _stop.set();return "Workflow stop signal set."
TOOL={"name":"windows_workflow_stop","description":"Set a local stop signal that cooperating Mark-LIV workflows can check.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_workflow_stop}
