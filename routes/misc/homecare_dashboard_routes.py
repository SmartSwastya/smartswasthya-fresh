# 📁 routes/homecare_dashboard_routes.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from tools.obvious_router import auto_route
from tools.smart_template import templates
from tools.auth import get_current_user
from database import get_db

from logic.homecare_logic import (
    get_homecare_profile_by_user,
    get_homecare_summary
)

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Router Setup                          ║
# ╚════════════════════════════════════════════════╝
router = APIRouter()


# ╔════════════════════════════════════════════════╗
# ║ SECTION: Homecare Dashboard                    ║
# ╚════════════════════════════════════════════════╝
@auto_route
@router.get("/homecare", response_class=HTMLResponse, name="homecare-dashboard")
async def homecare_dashboard_page(
    request: Request,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = get_homecare_profile_by_user(db, user["user_id"])
    summary = get_homecare_summary(profile.id if profile else 0)

    return templates.TemplateResponse("homecare_dashboard.html", {"request": request})
