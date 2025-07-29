# routes/dev/sync/get_task_summary_route.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/dev/task/summary")
def get_task_summary():
    return JSONResponse(content={"tasks": {"success": 40, "failed": 3, "pending": 5}})
