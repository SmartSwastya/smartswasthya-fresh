# 📁 routes/home_routes.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from tools.obvious_router import auto_route, auto_logic
from tools.smart_template import templates
from tools.auth import get_current_user_optional
from config import settings

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Router Setup                          ║
# ╚════════════════════════════════════════════════╝
router = APIRouter()


# ╔════════════════════════════════════════════════╗
# ║ SECTION: Public Home Page                      ║
# ╚════════════════════════════════════════════════╝
@auto_route
@auto_logic
@router.get("/", response_class=HTMLResponse)
async def home(request: Request, user: dict = Depends(get_current_user_optional)):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "user": user,
            "google_maps_api_key": settings.GOOGLE_GEO_API_KEY
        }
    )
