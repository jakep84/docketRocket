import os
import us
import yaml

# Make sure the 'rules' directory exists
rules_dir = "rules"
os.makedirs(rules_dir, exist_ok=True)

base_rule = {
    "rules": [
        {
            "event": "Complaint Filed",
            "deadlines": [
                {"name": "Defendant Response Due", "offset_days": 30}
            ]
        }
    ]
}

for state in us.states.STATES:
    filename = f"{state.name.lower().replace(' ', '_')}_civil.yaml"
    path = os.path.join(rules_dir, filename)
    data = {
        "jurisdiction": state.name,
        "case_type": "Civil",
        **base_rule
    }
    with open(path, "w") as f:
        yaml.dump(data, f)

print("Generated basic rules for all 50 states in /rules")
