# ╔════════════════════════════════════════════════╗
# ║ FILE: routes/account_routes.py                 ║
# ║ PURPOSE: Docker-safe placeholder removal       ║
# ╚════════════════════════════════════════════════╝

from fastapi import APIRouter
from tools.obvious_router import auto_route, auto_logic

router = APIRouter()

@auto_route
@auto_logic
@router.get("/account-dummy", operation_id="get_account-dummy")
async def dummy_account():
    return {"msg": "Account route active"}
