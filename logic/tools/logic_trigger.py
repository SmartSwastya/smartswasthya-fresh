# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from importlib import import_module
from tools.obvious_router import auto_logic

from tools.smart_logger import logger
from tools.smart_marker_injector import auto_route
from tools.obvious_router import auto_route

router = APIRouter(
    prefix="/logic",
    tags=["logic"]
)

# @auto_route
@router.post("/trigger-logic", operation_id="post_trigger-logic")
# @auto_logic
async def trigger_logic(request: Request):
    data = await request.json()
    logic_name = data.get("logic")
    action = data.get("action", "run")

    if not logic_name or action not in {"run", "apply"}:
        return JSONResponse(status_code=400, content={"status": "error", "message": "Missing or invalid parameters"})

    try:
        module = import_module(f"logic.{logic_name}")
        func = getattr(module, action, None)

        if not callable(func):
            return JSONResponse(status_code=404, content={"status": "error", "message": f"{action}() not found in {logic_name}"})

        func()  # run the logic (no args for now)
        logger.log(f"🧠 Logic {logic_name}.{action}() triggered", tag="info")
        return {"status": "success", "message": f"{logic_name}.{action}() executed"}

    except Exception as e:
        logger.log_exception(f"Trigger failure in {logic_name}.{action}()", e)
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

def run():
    return {"logic": "run() from logic_trigger", "status": "OK"}

def apply():
    return run()
