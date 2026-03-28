from pydantic import BaseModel
from typing import Optional, List, Literal

class EmailObservation(BaseModel):
    email_id: str
    subject: str
    body: str
    sender: str
    timestamp: str
    task_name: str
    task_description: str
    step_count: int
    max_steps: int

class EmailAction(BaseModel):
    action_type: Literal['classify','extract','draft']
    classification: Optional[Literal['urgent','normal','spam']] = None
    action_items: Optional[List[str]] = None
    draft_reply: Optional[str] = None

class EmailReward(BaseModel):
    reward: float
    done: bool
    info: dict
