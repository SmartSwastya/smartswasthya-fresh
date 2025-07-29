# "routes\ambulance\ambulance_dashboard.py"
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRoute
from typing import Optional
from sqlalchemy.orm import Session

from tools.auth import get_current_user
from tools.obvious_router import auto_route
from database import get_db

# Optional: Import models if available (can be enabled later)
# from models.ambulance import Ambulance, Driver

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Router + Template Config              ║
# ╚════════════════════════════════════════════════╝
router = APIRouter()
templates = Jinja2Templates(directory="templates")

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Ambulance Dashboard Route             ║
# ╚════════════════════════════════════════════════╝
@auto_route
@router.get("/ambulance", response_class=HTMLResponse, name="ambulance-dashboard")
async def ambulance_dashboard_page(
    request: Request,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # TODO: Replace these hardcoded values with real queries
    available_count = 18
    in_transit_count = 5
    drivers_count = 12

    fleet_info = [
        "Ambulance Types: ICU, Basic, Neonatal, etc.",
        "Maintenance Schedule",
        "Vehicle Health Status"
    ]

    emergency_info = [
        "Live Emergency Alerts",
        "Priority Dispatch System",
        "Auto-route via Google Maps"
    ]

    staff_info = [
        "Driver Availability & Status",
        "Certifications & Training",
        "Shift Assignments"
    ]

    biometric_info = [
        "Fingerprint or RFID Access",
        "Real-time Log System",
        "Central Monitoring Panel"
    ]

    live_tracking_status = "[Live Map Preview Placeholder]"

    return templates.TemplateResponse(
        "ambulance_dashboard.html",
        {
            "request": request,
            "user": user,
            "available_count": available_count,
            "in_transit_count": in_transit_count,
            "drivers_count": drivers_count,
            "fleet_info": fleet_info,
            "emergency_info": emergency_info,
            "staff_info": staff_info,
            "biometric_info": biometric_info,
            "live_tracking_status": live_tracking_status
        }
    )
