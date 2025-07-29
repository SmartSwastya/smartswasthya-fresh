# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# ✅ tools/task_reassigner.py

from database import SessionLocal
from models.dev_tasks import DevTask
from datetime import datetime
import os

LOG_FILE = "records/dev_logs/reassign_log.txt"

@auto_model
@auto_route
@auto_logic
def reassign_task(task_id: str, new_dev: str) -> bool:
    """
    Reassigns the task to a new developer and logs the change.
    Returns True if successful, False otherwise.
    """
    db = SessionLocal()
    task = db.query(DevTask).filter(DevTask.task_id == task_id).first()

    if not task:
        print(f"[❌] Task ID '{task_id}' not found.")
        db.close()
        return False

    old_dev = task.assigned_to or "unassigned"
    task.assigned_to = new_dev
    task.updated_at = datetime.utcnow()
    db.commit()
    db.close()

    # Ensure log directory exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    log_entry = f"{datetime.utcnow().isoformat()} | Task {task_id} reassigned from {old_dev} → {new_dev}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

    print(f"[✅] Task {task_id} successfully reassigned to {new_dev}")
    return True

