from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# ==================== 🔐 SYS004: Admin Task Logger Helper ====================

import json
from datetime import datetime

@auto_model
@auto_route
@auto_logic
def log_admin_task(task_name: str, admin_identity: str, payload: dict, task_id: str):
    log_entry = {
        "task_name": task_name,
        "admin": admin_identity,
        "payload": payload,
        "task_id": task_id,
        "timestamp": datetime.utcnow().isoformat()
    }

    log_file = "logs/admin_task_log.json"
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

