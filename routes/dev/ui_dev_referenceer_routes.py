# ╔════════════════════════════════════════════════╗
# ║ FILE: routes/dev/ui_dev_referenceer_routes.py  ║
# ║ PURPOSE: Render UI Dev Reference Viewer Page   ║
# ╚════════════════════════════════════════════════╝

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from tools.obvious_router import auto_route, auto_logic

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Router Init                           ║
# ╚════════════════════════════════════════════════╝
router = APIRouter(prefix="/dev/ui-dev-referenceer", tags=["UI Referenceer"])
templates = Jinja2Templates(directory="templates")

# ╔════════════════════════════════════════════════╗
# ║ ROUTE: UI Referenceer Page                     ║
# ╚════════════════════════════════════════════════╝
@auto_route
@auto_logic
@router.get("/", response_model=None)
async def show_ui_referenceer(request: Request):
    return templates.TemplateResponse("ui_dev_referenceer.html", {"request": request})
