# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# 📁 routes/admin/admin_notify.py

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from tools.obvious_router import auto_route
from handler import auto_model, auto_logic

router = APIRouter()


@auto_model
@auto_route
@auto_logic
@router.post("/admin/notify")
def send_admin_notification(message: str):
    return JSONResponse(content={
        "status": "sent",
        "message": f"Notification: {message}"
    })
