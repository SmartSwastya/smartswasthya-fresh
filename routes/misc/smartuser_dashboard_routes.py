# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# ────────────────────────────────────────────────────────────────
# 📁 FILE: routes/smartuser_dashboard_routes.py
# 📌 PURPOSE: Docker-safe placeholder removal
# ────────────────────────────────────────────────────────────────

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from services.user_profile_service import get_profile
from tools.auth import get_current_user  # assumes FastAPI Auth implemented
import logging
from fastapi import Depends

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# <smart.template>
@auto_model
@auto_route
@auto_logic
def calculate_age(dob):
    today = datetime.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

@router.get("/smart", operation_id="get_smart", response_class=HTMLResponse)
async def smartuser_dashboard_page(request: Request, user: dict = Depends(get_current_user)):
    logging.debug(f"User Data (current_user): {user}")
    profile = get_profile(user.id)
    age = calculate_age(user.dob) if user.dob else None

    return templates.TemplateResponse("smartuser_dashboard.html", {
        "request": request,
        "user": user,
        "profile": profile,
        "age": age,
        "prescriptions": getattr(user, "prescriptions", []),
        "family": getattr(user, "family_members", []),
        "appointments": getattr(user, "appointments", [])
    })
