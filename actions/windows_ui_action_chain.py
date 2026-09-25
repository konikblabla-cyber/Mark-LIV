"""Bounded Windows UI action chain with optional verification steps."""
import platform,time,pyautogui
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_ui_action_chain(parameters=None,**kwargs):
 p=parameters or {}; steps=p.get("steps",[])
 if not isinstance(steps,list) or len(steps)>20:return "steps must be a list of at most 20 actions."
 results=[]
 for i,s in enumerate(steps):
  if not isinstance(s,dict): return f"Invalid step {i+1}."
  a=str(s.get("action","")).lower()
  try:
   if a=="wait": time.sleep(max(0,min(float(s.get("seconds",.5)),10)))
   elif a=="press": pyautogui.press(str(s.get("key","enter")))
   elif a=="hotkey": pyautogui.hotkey(*[str(x) for x in s.get("keys",[])][:6])
   elif a=="type": pyautogui.write(str(s.get("text","")),interval=0.01)
   elif a=="click": pyautogui.click(int(s["x"]),int(s["y"]))
   else:return f"Unsupported step {i+1}: {a}"
   results.append(f"{i+1}:{a}")
  except Exception as e:return f"Stopped at step {i+1}: {e}"
 return "Completed: "+"; ".join(results)
TOOL={"name":"windows_ui_action_chain","description":"Execute up to 20 bounded normal Windows keyboard/mouse UI steps as one action chain.","parameters":{"type":"OBJECT","properties":{"steps":{"type":"ARRAY","items":{"type":"OBJECT"}}},"required":["steps"]},"handler":windows_ui_action_chain}
