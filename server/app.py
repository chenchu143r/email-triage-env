import sys, os
sys.path.insert(0, "/app")
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from typing import Optional
import uvicorn
from models import EmailObservation, EmailAction, EmailState
from server.environment import EmailTriageEnvironment, TASKS

app = FastAPI(title="Email Triage OpenEnv", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
env = EmailTriageEnvironment()

@app.get("/")
def root():
    return {"status": "ok", "name": "email-triage-env", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy", "service": "email-triage-env"}

@app.get("/openenv.yaml", response_class=PlainTextResponse)
def get_yaml():
    try:
        with open("/app/openenv.yaml") as f: return f.read()
    except:
        return "name: email-triage-env\nversion: 1.0.0\n"

@app.post("/reset")
def reset(task_name: Optional[str] = None):
    obs = env.reset(task_name=task_name)
    return obs.model_dump()

@app.post("/step")
def step(action: EmailAction):
    if env.current_task is None:
        raise HTTPException(status_code=400, detail="Call /reset first")
    obs, reward, done, info = env.step(action)
    return {"observation": obs.model_dump(), "reward": reward, "done": done, "info": info}

@app.get("/state")
def state():
    return env.state.model_dump()

@app.get("/tasks")
def tasks():
    return {"tasks": [{"name": t["name"], "description": t["description"], "difficulty": t["difficulty"]} for t in TASKS.values()]}

@app.post("/grader")
def grader(action: EmailAction):
    if env.current_task is None:
        raise HTTPException(status_code=400, detail="Call /reset first")
    obs, reward, done, info = env.step(action)
    return {"score": reward, "done": done, "info": info}

@app.get("/baseline")
def baseline():
    from server.environment import grade_task_1, grade_task_2, grade_task_3
    scores = {}
    total = sum(grade_task_1(eid, "urgent") for eid in TASKS["task_1_classify"]["email_ids"])
    scores["task_1_classify"] = round(total/len(TASKS["task_1_classify"]["email_ids"]), 2)
    scores["task_2_extract"] = grade_task_2(["review Q1 report", "schedule call with finance team", "update the dashboard", "submit design mockups", "update jira timeline", "send status report", "book client meeting"])
    scores["task_3_draft"] = grade_task_3("Dear Client, I sincerely apologize for the service outage. I acknowledge the significant disruption and losses this caused. We will investigate immediately, resolve this permanently, and discuss compensation. Please contact our dedicated support team today.")
    return {"baseline_scores": scores, "average": round(sum(scores.values())/len(scores), 2)}

def main():
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))

if __name__ == "__main__":
    main()
