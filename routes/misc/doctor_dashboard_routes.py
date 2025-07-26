# 📁 FILE: routes/doctor_dashboard_routes.py
# 📌 PURPOSE: Doctor dashboard route with profile & metrics

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session  # ✅ Required for `Depends(get_db)`

from tools.auth import get_current_user
from database import get_db
from logic.doctor_logic import (
    get_doctor_profile_by_user,
    get_doctor_metrics
)
from tools.obvious_router import auto_route

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@auto_route
@router.get("/doctor", response_class=HTMLResponse, name="doctor-dashboard")
# <smart.template>
async def doctor_dashboard_page(
    request: Request,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = get_doctor_profile_by_user(db, user["user_id"])
    metrics = get_doctor_metrics(user["user_id"])

    return templates.TemplateResponse(
        "doctor_dashboard.html",
        {
            "request": request,
            "user": user,
            "profile": profile,
            "metrics": metrics
        }
    )
