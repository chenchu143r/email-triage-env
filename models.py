from pydantic import BaseModel, Field
from typing import Optional, List, Literal

class EmailObservation(BaseModel):
    email_id: str = Field(description="Unique email identifier")
    subject: str = Field(description="Email subject line")
    body: str = Field(description="Email body content")
    sender: str = Field(description="Sender email address")
    timestamp: str = Field(description="Email timestamp")
    task_name: str = Field(description="Current task name")
    task_description: str = Field(description="What the agent must do")
    step_count: int = Field(description="Steps taken so far")
    max_steps: int = Field(description="Maximum steps allowed")
    done: bool = Field(default=False, description="Whether episode is complete")
    reward: float = Field(default=0.0, description="Last reward received")

class EmailAction(BaseModel):
    action_type: Literal["classify","extract","draft"] = Field(description="Type of action")
    classification: Optional[Literal["urgent","normal","spam"]] = Field(default=None)
    action_items: Optional[List[str]] = Field(default=None)
    draft_reply: Optional[str] = Field(default=None)

class EmailState(BaseModel):
    task_name: Optional[str] = None
    task_difficulty: Optional[str] = None
    current_email_id: Optional[str] = None
    step_count: int = 0
    max_steps: int = 10
    done: bool = False
    episode_rewards: List[float] = []
    cumulative_reward: float = 0.0
    available_tasks: List[str] = []
