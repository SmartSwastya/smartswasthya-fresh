# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.obvious_router import auto_logic
# PATCHED: routes/base_routes.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from tools.auth import get_current_user
from fastapi import Depends
from tools.smart_marker_injector import auto_route

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# @auto_route
@router.get("/base", operation_id="get_base", response_class=HTMLResponse)
# @auto_logic
# <smart.template>
async def base_template(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("base.html", {"request": request, "user": user})
