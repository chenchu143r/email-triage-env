from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from typing import Optional
import uvicorn, os, sys
sys.path.insert(0,".")
from models import EmailObservation, EmailAction
from environment import EmailTriageEnvironment

app=FastAPI(title="Email Triage OpenEnv",version="1.0.0")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])
env=EmailTriageEnvironment()

@app.get("/")
def root(): return {"status":"ok","name":"email-triage-env","version":"1.0.0"}

@app.get("/openenv.yaml", response_class=PlainTextResponse)
def openenv_yaml():
    return open("openenv.yaml").read()

@app.post("/reset")
def reset(task_name:Optional[str]=None):
    obs=env.reset(task_name=task_name); return obs.model_dump()

@app.post("/step")
def step(action:EmailAction):
    if env.current_task is None: raise HTTPException(status_code=400,detail="Call /reset first")
    obs,reward,done,info=env.step(action)
    return {"observation":obs.model_dump(),"reward":reward,"done":done,"info":info}

@app.get("/state")
def state(): return env.state()

@app.get("/tasks")
def tasks():
    from tasks import TASKS
    return {"tasks":[{"name":t["name"],"description":t["description"],"difficulty":t["difficulty"]} for t in TASKS.values()]}

@app.post("/grader")
def grader(action:EmailAction):
    if env.current_task is None: raise HTTPException(status_code=400,detail="Call /reset first")
    obs,reward,done,info=env.step(action)
    return {"score":reward,"done":done,"info":info}

@app.get("/baseline")
def baseline():
    from tasks import grade_task_1,grade_task_2,grade_task_3,TASKS
    scores={}
    total=sum(grade_task_1(eid,"urgent") for eid in TASKS["task_1_classify"]["email_ids"])
    scores["task_1_classify"]=round(total/len(TASKS["task_1_classify"]["email_ids"]),2)
    scores["task_2_extract"]=grade_task_2(["review Q1 report","schedule call with finance team","update the dashboard"])
    scores["task_3_draft"]=grade_task_3("Dear client, I sincerely apologize for the service outage. I acknowledge the downtime caused significant losses. We will compensate and resolve this. Please contact us to discuss.")
    return {"baseline_scores":scores,"average":round(sum(scores.values())/len(scores),2)}

if __name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=int(os.environ.get("PORT",7860)))
