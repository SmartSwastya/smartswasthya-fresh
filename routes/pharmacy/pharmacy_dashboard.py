# 📁 routes/pharmacy/pharmacy_dashboard.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from tools.obvious_router import auto_route, auto_logic
from tools.smart_template import templates
from tools.auth import get_current_user


# ╔════════════════════════════════════════════════╗
# ║ SECTION: Router Setup                          ║
# ╚════════════════════════════════════════════════╝
router = APIRouter()


# ╔════════════════════════════════════════════════╗
# ║ SECTION: Pharmacy Dashboard                    ║
# ╚════════════════════════════════════════════════╝
@auto_route
@auto_logic
@router.get("/pharma", response_class=HTMLResponse)
async def pharma_dashboard_page(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("pharmacy_dashboard.html", {"request": request})
