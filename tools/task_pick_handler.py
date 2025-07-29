# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
import json
from pathlib import Path
from datetime import datetime
from tools.smart_logger import SmartLogger

logger = SmartLogger("TaskPickHandler")

# JSON paths
PENDING_TASKS_FILE = Path("data/pending_tasks.json")
PICKED_LOG_FILE = Path("data/picked_tasks_log.json")

# Admin bypass emails
ADMIN_EMAILS = ["date.hrushikesh@gmail.com", "vkota2774@gmail.com"]

@auto_model
@auto_route
@auto_logic
def is_admin(email: str) -> bool:
    return email in ADMIN_EMAILS

@auto_model
@auto_route
@auto_logic
def load_json(path, default):
    try:
        return json.loads(path.read_text()) if path.exists() else default
    except Exception as e:
        logger.error(f"Failed to load {path}: {e}")
        return default

@auto_model
@auto_route
@auto_logic
def save_json(path, data):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2))
    except Exception as e:
        logger.error(f"Failed to save {path}: {e}")

@auto_model
@auto_route
@auto_logic
def pick_task_with_review(task_id: int, picked_by: str, email: str):
    tasks = load_json(PENDING_TASKS_FILE, [])
    for task in tasks:
        if task["id"] == task_id and task["status"] == "visible":
            task["status"] = "picked"
            task["picked_by"] = picked_by
            task["picked_at"] = datetime.now().isoformat()
            task["bypass_review"] = is_admin(email)
            save_json(PENDING_TASKS_FILE, tasks)

            log = load_json(PICKED_LOG_FILE, [])
            log.append({
                "task_id": task_id,
                "picked_by": picked_by,
                "email": email,
                "timestamp": datetime.now().isoformat(),
                "bypass_review": is_admin(email)
            })
            save_json(PICKED_LOG_FILE, log)

            logger.success(f"Task #{task_id} picked by {picked_by} ({'ADMIN' if is_admin(email) else 'dev'})")
            return True
    logger.warning(f"Task #{task_id} could not be picked (invalid or already picked)")
    return False

