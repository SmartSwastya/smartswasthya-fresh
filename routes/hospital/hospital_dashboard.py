# 📁 FILE: routes/hospital/hospital_dashboard_routes.py
# 📌 PURPOSE: Hospital dashboard route with profile & overview

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session  # ✅ FIX: Required for db param

from tools.auth import get_current_user
from database import get_db
from logic.hospital_logic import (
    get_hospital_profile_by_user,
    get_hospital_overview
)
from tools.obvious_router import auto_route

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@auto_route
@router.get("/hospital", response_class=HTMLResponse, name="hospital-dashboard")
# <smart.template>
async def hospital_dashboard_page(
    request: Request,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = get_hospital_profile_by_user(db, user["user_id"])
    overview = get_hospital_overview(profile.id if profile else 0)

    return templates.TemplateResponse("hospital_dashboard.html", {
        "request": request,
        "user": user,
        "profile": profile,
        "overview": overview
    })
