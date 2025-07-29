# route/dev/dev_alerts.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/dev/alerts")
def get_dev_alerts():
    return JSONResponse(content={"alerts": ["Error in sync", "Task failed", "Retry pending"]})
