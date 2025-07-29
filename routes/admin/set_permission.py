# routes/admin/set_permission.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/admin/permissions/set")
def set_permission(user_id: int, permission: str):
    return JSONResponse(content={"status": "success", "user_id": user_id, "permission": permission})
