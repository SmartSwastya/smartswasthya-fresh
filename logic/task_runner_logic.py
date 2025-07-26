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
# logic/task_runner_logic.py
from celery import current_app
from tools.smart_logger import SmartLogger

logger = SmartLogger("TaskRunnerLogic")

# @auto_logic
@auto_model
@auto_route
@auto_logic
def run_celery_task():
    try:
        logger.info("🎯 Firing Celery task 'cleanup_old_files'")
        task = current_app.send_task("tasks.cleanup_old_files")  # Make sure this task is registered
        logger.success(f"✅ Task sent: {task.id}")
        return {"status": "sent", "task_id": task.id}
    except Exception as e:
        logger.error(f"❌ Failed to run celery task: {str(e)}")
        return {"status": "error", "message": str(e)}
