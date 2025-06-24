from pydantic import BaseModel
from typing import List

class DeadlineRequest(BaseModel):
    jurisdiction: str
    case_type: str
    trigger_event: str
    trigger_date: str  # Format: YYYY-MM-DD

class Deadline(BaseModel):
    name: str
    due_date: str
    rule_applied: str

class DeadlineResponse(BaseModel):
    deadlines: List[Deadline]
