# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# ╭──────────────────────────────────────────────────────────╮
# │ 📂 ROUTE LAYER :: task_runner.py                         │
# │ Description: Task trigger endpoints for cleanup/test     │
# ╰──────────────────────────────────────────────────────────╯

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from logic.task_logic import (
    trigger_cleanup_task,
    trigger_cleanup_test,
    get_task_status,
)
from utils.auth_guard import get_admin_token_header
from tools.smart_marker_injector import auto_route
from tools.obvious_router import auto_route

router = APIRouter()

# ╭──────────────────────────────────────────────────────────╮
# │ 🧩 Input Model                                           │
# ╰──────────────────────────────────────────────────────────╯
class TaskInput(BaseModel):
    x: int
    y: int

# ╭──────────────────────────────────────────────────────────╮
# │ 🚀 POST /run-task                                        │
# ╰──────────────────────────────────────────────────────────╯
# @auto_route
@router.post("/run-task", operation_id="post_run-task")
@auto_model
@auto_route
@auto_logic
def run_task(payload: TaskInput, x_token: str = Depends(get_admin_token_header)):
    task_id = trigger_cleanup_task(x_token, payload.dict())
    return {"message": "Cleanup task triggered", "task_id": task_id}

# ╭──────────────────────────────────────────────────────────╮
# │ 🧪 GET /sys/cleanup-test                                 │
# ╰──────────────────────────────────────────────────────────╯
@router.get("/sys/cleanup-test", operation_id="get_sys_cleanup-test")
@auto_model
@auto_route
@auto_logic
def cleanup_test(x_token: str = Depends(get_admin_token_header)):
    task_id = trigger_cleanup_test(x_token)
    return {"message": "Test Cleanup task triggered", "task_id": task_id}

# ╭──────────────────────────────────────────────────────────╮
# │ 📊 GET /sys/task-status/{task_id}                        │
# ╰──────────────────────────────────────────────────────────╯
@router.get("/sys/task-status/{task_id}", operation_id="get_sys_task-status_{task_id}")
@auto_model
@auto_route
@auto_logic
def check_task_status(task_id: str, x_token: str = Depends(get_admin_token_header)):
    status = get_task_status(task_id)
    return status

