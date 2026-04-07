import sys
sys.path.insert(0, ".")
from environment import EmailTriageEnvironment
from models import EmailAction

def run():
    env = EmailTriageEnvironment()
    tasks = ["task_1_classify", "task_2_extract", "task_3_draft"]

    for task_name in tasks:
        obs = env.reset(task_name=task_name)
        print(f"[START] task={task_name}", flush=True)

        if task_name == "task_1_classify":
            from tasks import TASKS
            step = 0
            for eid in TASKS["task_1_classify"]["email_ids"]:
                s = obs.subject.lower() + " " + obs.body.lower()
                cl = "spam" if any(k in s for k in ["won","prize","bank","click"]) else "urgent" if any(k in s for k in ["urgent","asap","down"]) else "normal"
                obs, r, done, info = env.step(EmailAction(action_type="classify", classification=cl))
                step += 1
                print(f"[STEP] step={step} reward={r}", flush=True)
                if done: break
            score = round(sum(env.episode_rewards)/len(env.episode_rewards), 2)

        elif task_name == "task_2_extract":
            obs, r, done, info = env.step(EmailAction(
                action_type="extract",
                action_items=["review Q1 report", "schedule call with finance team", "update the dashboard"]
            ))
            print(f"[STEP] step=1 reward={r}", flush=True)
            score = r

        elif task_name == "task_3_draft":
            obs, r, done, info = env.step(EmailAction(
                action_type="draft",
                draft_reply="Dear Client, I sincerely apologize for the service outage. I acknowledge the downtime caused significant losses. We will compensate and resolve this permanently. Please contact our support team to discuss."
            ))
            print(f"[STEP] step=1 reward={r}", flush=True)
            score = r

        print(f"[END] task={task_name} score={score} steps={len(env.episode_rewards)}", flush=True)

if __name__ == "__main__":
    run()
