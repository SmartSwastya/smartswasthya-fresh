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
from celery_app import celery_app
from tools.smart_logger import SmartLogger
logger = SmartLogger("DummyTask")
# @odil_trace(run=True, apply=True)

# @auto_logic
@auto_model
@auto_route
@auto_logic
def run():
    logger.info("Running logic: dummy_task.run()")
    try:
        result = add.delay(2, 3)
        logger.info(f"Task dispatched with ID: {result.id}")
        return {"status": "dispatched", "task_id": result.id}
    except Exception as e:
        logger.error(f"Run error: {str(e)}")
        return {"status": "error", "message": str(e)}

@auto_model
@auto_route
@auto_logic
def apply():
    logger.info("Running logic: dummy_task.apply()")
    try:
        logger.info("Nothing to apply in dummy task")
        return {"status": "noop", "message": "Dummy apply acknowledged"}
    except Exception as e:
        logger.error(f"Apply error: {str(e)}")
        return {"status": "error", "message": str(e)}

@celery_app.task(name="add_numbers")
@auto_model
@auto_route
@auto_logic
def add(x, y):
    return x + y

