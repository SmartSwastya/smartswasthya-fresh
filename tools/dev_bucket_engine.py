# tools/dev_bucket_engine.py
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

logger = SmartLogger("DevBucketEngine")

# JSON Paths
PENDING_TASKS_FILE = Path("data/pending_tasks.json")
PICKED_LOG_FILE = Path("data/picked_tasks_log.json")

@auto_model
@auto_route
@auto_logic
def load_json(file_path, default):
    if not file_path.exists():
        logger.warning(f"{file_path} not found. Initializing empty.")
        return default
    try:
        return json.loads(file_path.read_text())
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}")
        return default

@auto_model
@auto_route
@auto_logic
def save_json(file_path, data):
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(data, indent=2))
    except Exception as e:
        logger.error(f"Error saving {file_path}: {e}")

@auto_model
@auto_route
@auto_logic
def get_all_pending_tasks():
    return load_json(PENDING_TASKS_FILE, [])

@auto_model
@auto_route
@auto_logic
def add_new_task(task):
    tasks = get_all_pending_tasks()
    tasks.append({
        "id": len(tasks) + 1,
        "description": task,
        "status": "visible",
        "created_at": datetime.now().isoformat()
    })
    save_json(PENDING_TASKS_FILE, tasks)
    logger.info(f"New task added: {task}")

@auto_model
@auto_route
@auto_logic
def pick_task(task_id, picked_by):
    tasks = get_all_pending_tasks()
    for task in tasks:
        if task["id"] == task_id and task["status"] == "visible":
            task["status"] = "picked"
            task["picked_by"] = picked_by
            task["picked_at"] = datetime.now().isoformat()
            save_json(PENDING_TASKS_FILE, tasks)

            picked_log = load_json(PICKED_LOG_FILE, [])
            picked_log.append({
                "task_id": task_id,
                "picked_by": picked_by,
                "timestamp": datetime.now().isoformat()
            })
            save_json(PICKED_LOG_FILE, picked_log)

            logger.success(f"Task #{task_id} picked by {picked_by}")
            return True
    logger.warning(f"Task #{task_id} could not be picked")
    return False

