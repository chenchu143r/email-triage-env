import random
from models import EmailObservation, EmailAction
from tasks import TASKS, get_email, grade_task_1, grade_task_2, grade_task_3

class EmailTriageEnvironment:
    def __init__(self):
        self.task_names=list(TASKS.keys()); self.current_task_name=None; self.current_task=None
        self.current_email_index=0; self.current_email=None; self.step_count=0
        self.max_steps=10; self.episode_rewards=[]; self.done=False
    def reset(self,task_name=None):
        self.current_task_name=task_name if task_name in TASKS else random.choice(self.task_names)
        self.current_task=TASKS[self.current_task_name]; self.current_email_index=0
        self.current_email=get_email(self.current_task['email_ids'][0])
        self.step_count=0; self.episode_rewards=[]; self.done=False
        return self._obs()
    def step(self,action):
        if self.done: return self._obs(),0.0,True,{'error':'Episode done'}
        self.step_count+=1; reward=0.0; info={}; tn=self.current_task_name
        if tn=='task_1_classify':
            if action.action_type=='classify' and action.classification:
                reward=grade_task_1(self.current_email['email_id'],action.classification)
                info={'correct':reward==1.0,'expected':self.current_task['expected'].get(self.current_email['email_id']),'got':action.classification}
                self.current_email_index+=1
                if self.current_email_index<len(self.current_task['email_ids']):
                    self.current_email=get_email(self.current_task['email_ids'][self.current_email_index])
                else: self.done=True
            else: reward=-0.1; info={'error':'Use classify'}
        elif tn=='task_2_extract':
            if action.action_type=='extract' and action.action_items is not None:
                reward=grade_task_2(action.action_items); info={'score':reward}; self.done=True
            else: reward=-0.1; info={'error':'Use extract'}
        elif tn=='task_3_draft':
            if action.action_type=='draft' and action.draft_reply:
                reward=grade_task_3(action.draft_reply); info={'score':reward}; self.done=True
            else: reward=-0.1; info={'error':'Use draft'}
        if self.step_count>=self.max_steps: self.done=True; info['timeout']=True
        self.episode_rewards.append(reward)
        return self._obs(),reward,self.done,info
    def state(self):
        return {'task_name':self.current_task_name,'task_difficulty':self.current_task['difficulty'] if self.current_task else None,'current_email_id':self.current_email['email_id'] if self.current_email else None,'step_count':self.step_count,'max_steps':self.max_steps,'done':self.done,'episode_rewards':self.episode_rewards,'cumulative_reward':sum(self.episode_rewards),'available_tasks':self.task_names}
    def _obs(self):
        if not self.current_email or not self.current_task:
            return EmailObservation(email_id='none',subject='Call reset()',body='',sender='',timestamp='',task_name='none',task_description='Call reset()',step_count=0,max_steps=self.max_steps)
        return EmailObservation(email_id=self.current_email['email_id'],subject=self.current_email['subject'],body=self.current_email['body'],sender=self.current_email['sender'],timestamp=self.current_email['timestamp'],task_name=self.current_task_name,task_description=self.current_task['description'],step_count=self.step_count,max_steps=self.max_steps)
