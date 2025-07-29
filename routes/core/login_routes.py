# ╔════════════════════════════════════════════════╗
# ║ FILE: routes/login_routes.py                  ║
# ║ PURPOSE: Login, Forgot Password & Token Auth  ║
# ╚════════════════════════════════════════════════╝

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Request, Form, Depends, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from models import User, LegacyUser, ActiveToken
from database import get_db
from utils.fast2sms_otp_handler import send_forgot_otp, verify_otp
from tools.auth import (
    create_access_token,
    get_current_user_optional
)
from passlib.hash import scrypt as passlib_scrypt
from werkzeug.security import check_password_hash, generate_password_hash

from tools.smart_marker_injector import auto_route
from handler import auto_logic
from tools.smart_template import templates

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Router Init                           ║
# ╚════════════════════════════════════════════════╝
router = APIRouter()

# ╔════════════════════════════════════════════════╗
# ║ SECTION: UI Pages                              ║
# ╚════════════════════════════════════════════════╝
@auto_route
@router.get("/login", operation_id="get_login", response_class=HTMLResponse)
@auto_logic
async def login_page(request: Request, user: Optional[dict] = Depends(get_current_user_optional)):
    return templates.TemplateResponse("login.html", {
        "request": request,         # 🔹 Required for all Jinja URL building
        "current_user": user        # 🔹 Used in base.html/navbar
    })

@auto_route
@router.get("/forgot_password", operation_id="get_forgot_password", response_class=HTMLResponse)
@auto_logic
async def forgot_password_page(request: Request, user: Optional[dict] = Depends(get_current_user_optional)):
    return templates.TemplateResponse("forgot_password.html", {"request": request, "user": user})


# ╔════════════════════════════════════════════════╗
# ║ SECTION: Logic Endpoints                       ║
# ╚════════════════════════════════════════════════╝
@auto_route
@router.post("/check-user", operation_id="post_check-user")
@auto_logic
async def check_user_exists(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    mobile = (data.get("mobile") or data.get("identity") or "").strip()

    if not mobile.isdigit() or len(mobile) != 10:
        return JSONResponse(status_code=400, content={"status": "invalid", "message": "Invalid mobile number"})

    user = db.query(User).filter_by(mobile=mobile).first()
    if user:
        return {"status": "existing" if user.password else "create"}

    legacy = db.query(LegacyUser).filter_by(mobile=mobile).first()
    return {"status": "create" if legacy else "not_found"}


@auto_route
@router.post("/login", operation_id="post_login")
@auto_logic
async def login_user(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    mobile = (data.get("identity") or data.get("mobile") or "").strip()
    password = data.get("password", "")

    if not mobile or not password:
        return JSONResponse(status_code=400, content={"status": "fail", "message": "Mobile and password required"})

    user = db.query(User).filter_by(mobile=mobile).first()
    if not user:
        return JSONResponse(status_code=404, content={"status": "fail", "message": "User not found"})

    valid_pw = False
    if user.password:
        patched = user.password
        if patched.startswith("scrypt:"):
            patched = f"${patched}"
        try:
            if patched.startswith("$pbkdf2:") or patched.startswith("pbkdf2:"):
                valid_pw = check_password_hash(patched, password)
            elif patched.startswith("$scrypt$") or patched.startswith("scrypt:"):
                valid_pw = passlib_scrypt.verify(password, patched)
                if valid_pw:
                    user.password = generate_password_hash(password, method="pbkdf2:sha256")
                    db.commit()
        except Exception:
            pass

    if not valid_pw:
        return JSONResponse(status_code=401, content={"status": "fail", "message": "Incorrect password"})

    token = create_access_token(user.id, user.role)
    if not token:
        return JSONResponse(status_code=500, content={"status": "fail", "message": "Token generation error"})

    try:
        db.query(ActiveToken).filter_by(user_id=user.id).delete()
        db.flush()
        db.add(ActiveToken(user_id=user.id, token=token))
        db.commit()
    except Exception:
        db.rollback()
        return JSONResponse(status_code=500, content={"status": "fail", "message": "Token storage error"})

    return {"status": "success", "token": token, "redirect": "/smartuser_dashboard"}


@auto_route
@router.post("/set-password", operation_id="post_set-password")
@auto_logic
async def set_password(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    mobile = (data.get("mobile") or data.get("identity") or "").strip()
    password = data.get("password", "")

    if not mobile or not password:
        return JSONResponse(status_code=400, content={"status": "fail", "message": "Mobile and password required"})

    user = db.query(User).filter_by(mobile=mobile).first()
    if not user:
        legacy = db.query(LegacyUser).filter_by(mobile=mobile).first()
        if legacy:
            new_user = User(
                full_name=legacy.name,
                mobile=legacy.mobile,
                email=legacy.email,
                role=legacy.role,
                password=generate_password_hash(password, method="pbkdf2:sha256"),
                signup_source="legacy",
                is_verified=True
            )
            db.add(new_user)
            db.delete(legacy)
            db.commit()
            return {"status": "success", "redirect": "/smartuser_dashboard"}

        return JSONResponse(status_code=404, content={"status": "fail", "message": "User not found"})

    if user.password:
        return JSONResponse(status_code=400, content={"status": "fail", "message": "Password already set"})

    user.password = generate_password_hash(password, method="pbkdf2:sha256")
    db.commit()
    return {"status": "success", "redirect": "/smartuser_dashboard"}


@auto_route
@router.get("/send-forgot-otp", operation_id="get_send-forgot-otp")
@auto_logic
async def send_forgot_password_otp(mobile: str = Query(...), db: Session = Depends(get_db)):
    name = "Smart User"
    if not mobile.isdigit() or len(mobile) != 10:
        return JSONResponse(status_code=400, content={"status": "error", "message": "Invalid mobile number"})

    result = send_forgot_otp(mobile, name)
    return result


@auto_route
@router.get("/reset-password", operation_id="get_reset-password")
@auto_logic
async def reset_password(
    mobile: str = Query(...),
    password: str = Query(...),
    otp: str = Query(...),
    db: Session = Depends(get_db)
):
    otp_result = verify_otp(mobile, otp)
    if otp_result.get("status") != "verified":
        return JSONResponse(status_code=400, content={"success": False, "message": "Invalid OTP"})

    user = db.query(User).filter_by(mobile=mobile).first()
    if not user:
        return JSONResponse(status_code=404, content={"success": False, "message": "User not found"})

    user.password = generate_password_hash(password, method="pbkdf2:sha256")
    db.commit()
    return {"success": True, "message": "Password reset successful!", "redirect": "/login"}
