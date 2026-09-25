"""Bounded Windows mouse action sequence."""
import platform,time
import pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_mouse_sequence(parameters=None,**kwargs):
 p=parameters or {}; actions=p.get("actions",[])
 if not isinstance(actions,list) or len(actions)>20:return "actions must contain at most 20 items."
 for a in actions:
  if not isinstance(a,dict):continue
  kind=str(a.get("type","")).lower();x=int(a.get("x",0));y=int(a.get("y",0))
  if kind=="click":pyautogui.click(x,y)
  elif kind=="double_click":pyautogui.doubleClick(x,y)
  elif kind=="right_click":pyautogui.rightClick(x,y)
  elif kind=="move":pyautogui.moveTo(x,y,duration=.1)
  elif kind=="scroll":pyautogui.scroll(max(-20,min(20,int(a.get("amount",0)))))
  time.sleep(.05)
 return f"Executed {len(actions)} mouse actions."
TOOL={"name":"windows_mouse_sequence","description":"Execute a bounded sequence of normal mouse actions on Windows.","parameters":{"type":"OBJECT","properties":{"actions":{"type":"ARRAY","items":{"type":"OBJECT"}}}},"handler":windows_mouse_sequence}
