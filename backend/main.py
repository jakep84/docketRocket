from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta
import yaml

app = FastAPI()

class DeadlineRequest(BaseModel):
    jurisdiction: str
    case_type: str
    trigger_event: str
    trigger_date: str

class Deadline(BaseModel):
    name: str
    due_date: str
    rule_applied: str

class DeadlineResponse(BaseModel):
    deadlines: List[Deadline]

@app.post("/generate-deadlines/", response_model=DeadlineResponse)
def generate_deadlines(data: DeadlineRequest):
    try:
        with open(f"rules/{data.jurisdiction.lower().replace(' ', '_')}_{data.case_type.lower()}.yaml", "r") as f:
            ruleset = yaml.safe_load(f)
    except FileNotFoundError:
        return {"deadlines": []}

    deadlines = []
    base_date = datetime.strptime(data.trigger_date, "%Y-%m-%d")

    for rule in ruleset["rules"]:
        if rule["event"].lower() == data.trigger_event.lower():
            for deadline in rule["deadlines"]:
                due_date = base_date + timedelta(days=deadline["offset_days"])
                deadlines.append(Deadline(
                    name=deadline["name"],
                    due_date=due_date.strftime("%Y-%m-%d"),
                    rule_applied=f"{deadline['offset_days']} days after {data.trigger_event}"
                ))

    return DeadlineResponse(deadlines=deadlines)
