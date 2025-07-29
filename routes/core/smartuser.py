# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
# ────────────────────────────────────────────────
# Filename: routes/smartuser.py
# Description: Routes for SmartUser registration & login
# ────────────────────────────────────────────────
import tools.auth as auth
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserLogin
from database import get_db
from tools.smart_marker_injector import auto_route
from tools.obvious_router import auto_route
from tools.obvious_router import auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model

router = APIRouter(
    prefix="/smartuser",
#region auto_route
    tags=["Smart User"]
)

# @auto_function
# ────────────────────────────────────────────────
# Route: Register a new user
# ────────────────────────────────────────────────
# @auto_route
@router.post("/register", operation_id="post_register")
@auto_model
@auto_route
@auto_logic
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = auth.register_user_logic(db, user)
    return {"message": "🎉 Registered successfully", "user_id": new_user.id}

