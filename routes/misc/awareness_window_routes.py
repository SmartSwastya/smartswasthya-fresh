# 📁 routes/awareness_window_routes.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse  # ✅ FIXED
from fastapi.templating import Jinja2Templates
from tools.obvious_router import auto_route
from tools.obvious_router import auto_logic

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@auto_route
@router.get("/awareness", response_class=HTMLResponse)
# @auto_logic
# <smart.template>
async def awareness_page(request: Request):
    return templates.TemplateResponse("awareness_window.html", {"request": request})
