# 📁 FILE: routes/lab/lab_dashboard_routes.py
# 📌 PURPOSE: Lab dashboard with profile and test result summary

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session  # ✅ FIX: Required for db injection

from tools.auth import get_current_user
from database import get_db
from logic.lab_logic import get_lab_profile_by_user, get_recent_lab_tests

from tools.obvious_router import auto_route

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@auto_route
@router.get("/lab", response_class=HTMLResponse, name="lab-dashboard")
# <smart.template>
async def lab_dashboard_page(
    request: Request,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = get_lab_profile_by_user(db, user["user_id"])
    test_results = get_recent_lab_tests(db, profile.id if profile else 0)

    return templates.TemplateResponse("lab_dashboard.html", {
        "request": request,
        "user": user,
        "profile": profile,
        "test_results": test_results
    })
