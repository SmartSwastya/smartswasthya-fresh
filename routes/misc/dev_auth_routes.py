# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.obvious_router import auto_logic
# 📁 FILE: routes/dev_auth_routes.py

from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_302_FOUND
from database import get_db
from tools.auth import verify_password, create_access_token
from logic.helper import get_user_by_email
from tools.auth import get_current_user
from fastapi import Depends
from tools.smart_marker_injector import auto_route

templates = Jinja2Templates(directory="templates")
router = APIRouter()

# 🔐 Developer Login Page (GET)
# @auto_route
@router.get("/dev-login", operation_id="get_dev-login", response_class=HTMLResponse)
# @auto_logic
# <smart.template>
async def show_dev_login(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("dev_login.html", {"request": request, "user": user})

# 🔐 Admin Login Page (GET)
@router.get("/admin-login", operation_id="get_admin-login", response_class=HTMLResponse)
async def show_admin_login(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("admin_login.html", {"request": request, "user": user})

# 🔐 Developer Login (POST)
@router.post("/dev-login", operation_id="post_dev-login", response_class=HTMLResponse)
async def developer_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = get_user_by_email(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "dev_login.html", {"request": request, "error": "Invalid credentials"}
        )

    access_token = create_access_token(data={"sub": user.email, "role": "developer"})
    response = RedirectResponse(url="/dev-bucket/ui", status_code=HTTP_302_FOUND)
# @auto_flag: hardcoded_secrets [key]
# ⚠️ Hardcoded secret? Move to environment config
# @auto_flag: hardcoded_secrets [key]
# ⚠️ Hardcoded secret? Move to environment config
# @auto_flag: hardcoded_secrets [key]
# ⚠️ Hardcoded secret? Move to environment config
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response

# 🔐 Admin Login (POST)
@router.post("/admin-login", operation_id="post_admin-login", response_class=HTMLResponse)
async def admin_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = get_user_by_email(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "admin_login.html", {"request": request, "error": "Invalid credentials"}
        )

    access_token = create_access_token(data={"sub": user.email, "role": "admin"})
    response = RedirectResponse(url="/admin-trace", status_code=HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response
