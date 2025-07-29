# ╔════════════════════════════════════════════════╗
# ║ FILE: routes/admin/admin_trace_routes.py       ║
# ║ PURPOSE: Admin Permission Toggle + Trace View  ║
# ╚════════════════════════════════════════════════╝

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from tools.obvious_router import auto_route
from handler import auto_model, auto_logic
from tools.auth import get_current_user
from database import get_db

from logic.admin_trace_logic import set_permission, get_permissions
from models.users import User
from schemas.user import UserOut

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Router Init                           ║
# ╚════════════════════════════════════════════════╝
router = APIRouter(prefix="/admin-trace", tags=["Admin Trace"])


# ╔════════════════════════════════════════════════╗
# ║ SECTION: Request Models                        ║
# ╚════════════════════════════════════════════════╝
class TogglePermissionInput(BaseModel):
    key: str
    value: bool


# ╔════════════════════════════════════════════════╗
# ║ SECTION: Routes                                ║
# ╚════════════════════════════════════════════════╝
@auto_model
@auto_route
@auto_logic
@router.post("/set-permission", operation_id="post_set-permission")
def set_permission_route(
    payload: TogglePermissionInput,
    current_user: UserOut = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    set_permission(current_user.id, payload.key, payload.value)
    return {"message": f"{payload.key} set to {payload.value}"}


@auto_model
@auto_route
@auto_logic
@router.get("/dev-context", operation_id="get_dev-context")
def dev_context(
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return get_active_developers_with_permissions(db)


@auto_model
@auto_route
@auto_logic
@router.get("/get-permissions", operation_id="get_get-permissions")
def get_permission_route(current_user: UserOut = Depends(get_current_user)):
    return get_permissions(current_user.id)


@auto_model
@auto_route
@auto_logic
def get_active_developers_with_permissions(db: Session) -> list[dict]:
    developers = db.query(User).filter(User.is_active == True, User.is_admin == False).all()
    return [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "permissions": get_permissions(u.id)
        }
        for u in developers
    ]