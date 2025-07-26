# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from tools.smart_marker_injector import auto_route
from tools.obvious_router import auto_route
from tools.obvious_router import auto_logic

router = APIRouter(prefix="/dev", tags=["BaseCtrl"])
templates = Jinja2Templates(directory="templates")

# @auto_route
@router.get("/basectrl")
# @auto_logic
async def show_basectrl_editor(request: Request):
    return templates.TemplateResponse("basectrl.html", {"request": request})
