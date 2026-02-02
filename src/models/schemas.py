from typing import List, Optional
from pydantic import BaseModel, Field

class TaskSpec(BaseModel):
    task_id: str = Field(..., description="Unique identifier for the task request")
    description: str = Field(..., description="Detailed description of the task")
    acceptance_criteria: List[str] = Field(..., description="List of specific criteria to verify success")
    budget: float = Field(..., description="Maximum budget for the task")
    deadline: str = Field(..., description="Deadline for the task")
    required_skills: List[str] = Field(default_factory=list, description="List of required skills")

class Bid(BaseModel):
    bid_id: str = Field(..., description="Unique ID for the bid")
    task_id: str = Field(..., description="ID of the task this bid is for")
    agent_id: str = Field(..., description="ID of the worker agent")
    price: float = Field(..., description="Proposed price")
    timeline: str = Field(..., description="Proposed timeline")
    confidence: float = Field(..., description="Confidence score (0-1)")
    plan: str = Field(..., description="High-level execution plan")

class NegotiationStep(BaseModel):
    step_id: int
    sender: str
    recipient: str
    content: str
    offer_price: Optional[float] = None

class Contract(BaseModel):
    contract_id: str
    task_id: str
    selected_worker: str
    deliverables: List[str]
    tests: List[str]
    payment: float
    penalty_rules: List[str]
    status: str = "pending" # pending, active, completed, failed, disputed

class ExecutionResult(BaseModel):
    task_id: str
    worker_id: str
    output: str
    artifacts: List[str] = []

class ValidationResult(BaseModel):
    task_id: str
    passed: bool
    score: float
    issues: List[str]
    retry_allowed: bool

class AgentStats(BaseModel):
    agent_id: str
    tasks_completed: int = 0
    success_rate: float = 0.0
    avg_score: float = 0.0
    disputes: int = 0
