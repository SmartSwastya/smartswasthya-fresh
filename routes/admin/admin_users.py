# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# 📁 routes/admin/admin_users.py

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from tools.obvious_router import auto_route
from handler import auto_model, auto_logic

router = APIRouter()


@auto_model
@auto_route
@auto_logic
@router.get("/admin/users")
def list_admin_users():
    return JSONResponse(content={
        "users": ["admin1", "admin2", "admin3"]
    })
