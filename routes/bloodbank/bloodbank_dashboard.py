# 📁 routes/bloodbank/bloodbank_dashboard_routes.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from tools.auth import get_current_user
from database import get_db
from logic.bloodbank_logic import (
    get_bloodbank_profile_by_user,
    get_blood_stock_summary
)
from tools.obvious_router import auto_route

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@auto_route
@router.get("/bloodbank", response_class=HTMLResponse, name="bloodbank-dashboard")
# <smart.template>
async def bloodbank_dashboard_page(
    request: Request,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = get_bloodbank_profile_by_user(db, user["user_id"])
    blood_summary = get_blood_stock_summary(profile.id if profile else 0)

    return templates.TemplateResponse(
        "bloodbank_dashboard.html",
        {
            "request": request,
            "user": user,
            "profile": profile,
            "blood_summary": blood_summary
        }
    )
