# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.obvious_router import auto_logic
#region auto_route
# ===================================================================
# 📁 FILE: routes/scan_results_routes.py
# 📌 PURPOSE: Handles routes for scan_results.html
# ===================================================================

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from tools.auth import get_current_user
from fastapi import Depends
from tools.smart_marker_injector import auto_route

router = APIRouter()

# ------------------ Router & Template Setup -----------------------
scan_results_router = APIRouter(prefix="/scan-results", tags=["Scan Results"])
templates = Jinja2Templates(directory="templates")

# ------------------ Route: /scan_results --------------------------
@scan_results_router.get("/scan_results", response_class=HTMLResponse)
# @auto_logic
# <smart.template>
async def render_scan_results(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("scan_results.html", {"request": request, "user": user})
