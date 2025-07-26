# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# File: tools/devops/remove_null_dev_tasks.py

from database import SessionLocal
from models.dev_tasks import DevTask

@auto_model
@auto_route
@auto_logic
def clean_null_task_ids():
    db = SessionLocal()
    deleted = db.query(DevTask).filter(DevTask.task_id == None).delete()
    db.commit()
    db.close()
    print(f"✅ Deleted {deleted} row(s) with NULL task_id")

if __name__ == "__main__":
    clean_null_task_ids()

