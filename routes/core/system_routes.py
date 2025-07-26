# 📄 File: routes/system_routes.py
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter

router = APIRouter()

@router.get("/ping", operation_id="get_ping")
async def get_ping():
    return {"message": "pong"}
