import sys, os
sys.path.insert(0, ".")
from openai import OpenAI
from environment import EmailTriageEnvironment
from models import EmailAction

# Use hackathon's LLM proxy
client = OpenAI(
    base_url=os.environ.get("API_BASE_URL", "https://api.openai.com/v1"),
    api_key=os.environ.get("API_KEY", "dummy")
)

def llm_classify(subject, body):
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":f"Classify this email as urgent, normal, or spam. Reply with one word only.\nSubject: {subject}\nBody: {body}"}],
        max_tokens=10
    )
    result = resp.choices[0].message.content.strip().lower()
    for label in ["urgent","spam","normal"]:
        if label in result:
            return label
    return "normal"

def llm_extract(body):
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":f"Extract action items from this email. List each on a new line.\n{body}"}],
        max_tokens=100
    )
    items = resp.choices[0].message.content.strip().split("\n")
    return [i.strip("- ").strip() for i in items if i.strip()]

def llm_draft(subject, body, sender):
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":f"Write a professional reply to this complaint email.\nFrom: {sender}\nSubject: {subject}\nBody: {body}"}],
        max_tokens=200
    )
    return resp.choices[0].message.content.strip()

def run():
    env = EmailTriageEnvironment()
    from tasks import TASKS

    # Task 1
    task_name = "task_1_classify"
    obs = env.reset(task_name=task_name)
    print(f"[START] task={task_name}", flush=True)
    step = 0
    for eid in TASKS["task_1_classify"]["email_ids"]:
        cl = llm_classify(obs.subject, obs.body)
        obs, r, done, info = env.step(EmailAction(action_type="classify", classification=cl))
        step += 1
        print(f"[STEP] step={step} reward={r}", flush=True)
        if done: break
    score = round(sum(env.episode_rewards)/max(len(env.episode_rewards),1), 2)
    print(f"[END] task={task_name} score={score} steps={step}", flush=True)

    # Task 2
    task_name = "task_2_extract"
    obs = env.reset(task_name=task_name)
    print(f"[START] task={task_name}", flush=True)
    items = llm_extract(obs.body)
    obs, r, done, info = env.step(EmailAction(action_type="extract", action_items=items))
    print(f"[STEP] step=1 reward={r}", flush=True)
    print(f"[END] task={task_name} score={r} steps=1", flush=True)

    # Task 3
    task_name = "task_3_draft"
    obs = env.reset(task_name=task_name)
    print(f"[START] task={task_name}", flush=True)
    draft = llm_draft(obs.subject, obs.body, obs.sender)
    obs, r, done, info = env.step(EmailAction(action_type="draft", draft_reply=draft))
    print(f"[STEP] step=1 reward={r}", flush=True)
    print(f"[END] task={task_name} score={r} steps=1", flush=True)

if __name__ == "__main__":
    run()
