# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_logic
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from tools.obvious_router import auto_logic
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# ╭──────────────────────────────────────────────────────────╮
# │ 📂 LOGIC LAYER :: task_logic.py                          │
# │ Description: Handles task execution and status tracking │
# ╰──────────────────────────────────────────────────────────╯

from celery.result import AsyncResult
from tasks.cleanup_task import cleanup_old_files
from utils.logger_helper import log_admin_task
from tools.smart_logger import SmartLogger

logger = SmartLogger("TaskLogic")
# @odil_trace(run=True, apply=True)

# @auto_logic
@auto_model
@auto_route
@auto_logic
def run(*args, **kwargs):
    logger.info("Running task_logic.run() — Placeholder logic")
    return {
        "status": "success",
        "message": "Task runner executed (run). No actual task triggered."
    }

@auto_model
@auto_route
@auto_logic
def apply(*args, **kwargs):
    logger.info("Running task_logic.apply() — Placeholder logic")
    return {
        "status": "success",
        "message": "Task runner applied (apply). No changes applied."
    }

# ╭──────────────────────────────────────────────────────────╮
# │ 🚀 Trigger Cleanup Task                                  │
# ╰──────────────────────────────────────────────────────────╯
@auto_model
@auto_route
@auto_logic
def trigger_cleanup_task(x_token: str, payload: dict):
    task = cleanup_old_files.delay()
    log_admin_task(
        task_name="cleanup_old_files",
        admin_identity=x_token,
        payload=payload,
        task_id=task.id
    )
    return task.id

# ╭──────────────────────────────────────────────────────────╮
# │ 🧪 Test Cleanup Trigger                                  │
# ╰──────────────────────────────────────────────────────────╯
@auto_model
@auto_route
@auto_logic
def trigger_cleanup_test(x_token: str):
    task = cleanup_old_files.delay()
    log_admin_task(
        task_name="cleanup_old_files_test",
        admin_identity=x_token,
        payload={},
        task_id=task.id
    )
    return task.id

# ╭──────────────────────────────────────────────────────────╮
# │ 📊 Check Task Status                                     │
# ╰──────────────────────────────────────────────────────────╯
@auto_model
@auto_route
@auto_logic
def get_task_status(task_id: str):
    result = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.successful() else None
    }

