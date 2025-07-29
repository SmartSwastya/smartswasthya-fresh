# 📁 FILE: routes/family_dashboard_routes.py
# 📌 PURPOSE: Family dashboard showing health records and emergency contacts

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session  # ✅ Required for DB injection

from tools.auth import get_current_user
from database import get_db
from logic.family_logic import (
    get_family_health_status,
    get_emergency_contacts
)
from tools.obvious_router import auto_route

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@auto_route
@router.get("/family", response_class=HTMLResponse, name="family-dashboard")
# <smart.template>
async def family_dashboard_page(
    request: Request,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    health_records = get_family_health_status(db, user["user_id"])
    emergency_contacts = get_emergency_contacts(db, user["user_id"])

    return templates.TemplateResponse("family_dashboard.html", {
        "request": request,
        "user": user,
        "health_records": health_records,
        "emergency_contacts": emergency_contacts
    })
