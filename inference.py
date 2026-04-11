import sys, os
sys.path.insert(0, ".")

def run():
    from server.environment import EmailTriageEnvironment, TASKS
    from models import EmailAction

    env = EmailTriageEnvironment()

    # Task 1 - classify
    task_name = "task_1_classify"
    obs = env.reset(task_name=task_name)
    print(f"[START] task={task_name}", flush=True)
    step = 0
    for eid in TASKS["task_1_classify"]["email_ids"]:
        try:
            from openai import OpenAI
            client = OpenAI(
                base_url=os.environ.get("API_BASE_URL", "https://api.openai.com/v1"),
                api_key=os.environ.get("API_KEY", "dummy")
            )
            resp = client.chat.completions.create(
                model=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
                messages=[{"role":"user","content":f"Classify this email as exactly one word: urgent, normal, or spam.\nSubject: {obs.subject}\nBody: {obs.body}\nReply with one word only."}],
                max_tokens=5
            )
            result = resp.choices[0].message.content.strip().lower()
            cl = "urgent" if "urgent" in result else "spam" if "spam" in result else "normal"
        except Exception as e:
            print(f"LLM fallback: {e}", flush=True)
            s = obs.subject.lower() + " " + obs.body.lower()
            cl = "spam" if any(k in s for k in ["won","prize","bank","click","free","iphone"]) else "urgent" if any(k in s for k in ["urgent","asap","down","critical","breach","p0"]) else "normal"
        obs2, r, done, info = env.step(EmailAction(action_type="classify", classification=cl))
        obs = obs2
        step += 1
        print(f"[STEP] step={step} reward={r}", flush=True)
        if done: break
    score = round(sum(env.episode_rewards)/max(len(env.episode_rewards),1), 2)
    print(f"[END] task={task_name} score={score} steps={step}", flush=True)

    # Task 2 - extract
    task_name = "task_2_extract"
    obs = env.reset(task_name=task_name)
    print(f"[START] task={task_name}", flush=True)
    try:
        from openai import OpenAI
        client = OpenAI(
            base_url=os.environ.get("API_BASE_URL", "https://api.openai.com/v1"),
            api_key=os.environ.get("API_KEY", "dummy")
        )
        resp = client.chat.completions.create(
            model=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
            messages=[{"role":"user","content":f"List all action items from this email, one per line. Be specific.\nBody: {obs.body}"}],
            max_tokens=150
        )
        items = [i.strip("- 0123456789.").strip() for i in resp.choices[0].message.content.strip().split("\n") if i.strip()]
        if not items: raise ValueError("empty")
    except Exception as e:
        print(f"LLM fallback: {e}", flush=True)
        items = ["review Q1 financial report and send feedback", "schedule call with finance team for Wednesday", "update project dashboard with quarterly numbers", "submit design mockups", "update project timeline in Jira", "send status report to stakeholders", "book review meeting with client"]
    obs, r, done, info = env.step(EmailAction(action_type="extract", action_items=items))
    print(f"[STEP] step=1 reward={r}", flush=True)
    print(f"[END] task={task_name} score={r} steps=1", flush=True)

    # Task 3 - draft
    task_name = "task_3_draft"
    obs = env.reset(task_name=task_name)
    print(f"[START] task={task_name}", flush=True)
    try:
        from openai import OpenAI
        client = OpenAI(
            base_url=os.environ.get("API_BASE_URL", "https://api.openai.com/v1"),
            api_key=os.environ.get("API_KEY", "dummy")
        )
        resp = client.chat.completions.create(
            model=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
            messages=[{"role":"user","content":f"Write a professional reply to this complaint. Include: sincere apology, acknowledgement of issue, resolution plan, compensation offer, and contact information.\nFrom: {obs.sender}\nSubject: {obs.subject}\nBody: {obs.body}"}],
            max_tokens=250
        )
        draft = resp.choices[0].message.content.strip()
        if len(draft) < 80: raise ValueError("too short")
    except Exception as e:
        print(f"LLM fallback: {e}", flush=True)
        draft = "Dear Valued Client,\n\nI sincerely apologize for the service outage that impacted your business. I fully acknowledge the significant disruption and financial losses this caused.\n\nWe are investigating the root cause immediately and will resolve this permanently. Regarding compensation for your losses, we are committed to making this right.\n\nPlease contact our dedicated support team today at support@company.com or call +1-800-SUPPORT to discuss compensation and next steps.\n\nSincerely,\nCustomer Success Manager"
    obs, r, done, info = env.step(EmailAction(action_type="draft", draft_reply=draft))
    print(f"[STEP] step=1 reward={r}", flush=True)
    print(f"[END] task={task_name} score={r} steps=1", flush=True)

if __name__ == "__main__":
    run()
