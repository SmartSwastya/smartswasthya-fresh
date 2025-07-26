import json
from datetime import datetime
from pathlib import Path

LOG_PATH = Path("logs/picked_tasks_log.json")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def log_task_action(task_id, action, new_status=None, notes=None):
    log_entry = {
        "task_id": task_id,
        "action": action,
        "status": new_status,
        "timestamp": datetime.utcnow().isoformat(),
        "notes": notes,
    }

    if LOG_PATH.exists():
        with open(LOG_PATH, "r+", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
            logs.append(log_entry)
            f.seek(0)
            json.dump(logs, f, indent=2)
    else:
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            json.dump([log_entry], f, indent=2)
