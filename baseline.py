import sys; sys.path.insert(0,'.')
from environment import EmailTriageEnvironment
from models import EmailAction
from tasks import TASKS
env=EmailTriageEnvironment(); results={}
obs=env.reset(task_name='task_1_classify'); rewards=[]
for eid in TASKS['task_1_classify']['email_ids']:
    s=obs.subject.lower()+' '+obs.body.lower()
    cl='spam' if any(k in s for k in ['won','prize','bank','click']) else 'urgent' if any(k in s for k in ['urgent','asap','down']) else 'normal'
    obs,r,done,info=env.step(EmailAction(action_type='classify',classification=cl))
    rewards.append(r)
    if done: break
results['task_1_classify']=round(sum(rewards)/len(rewards),2)
obs=env.reset(task_name='task_2_extract')
obs,r,d,i=env.step(EmailAction(action_type='extract',action_items=['review Q1 report','schedule call with finance team','update the dashboard']))
results['task_2_extract']=r
obs=env.reset(task_name='task_3_draft')
obs,r,d,i=env.step(EmailAction(action_type='draft',draft_reply='Dear Client, I sincerely apologize for the service outage. I acknowledge the downtime caused losses. We will compensate and resolve this permanently. Please contact our support team to discuss.'))
results['task_3_draft']=r
for t,s in results.items(): print(f'{t}: {s:.2f}')
print(f'AVERAGE: {sum(results.values())/len(results):.2f}')
