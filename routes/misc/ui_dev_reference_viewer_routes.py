# routes/ui_dev_reference_viewer_routes.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from tools.auth import get_current_user_optional
from fastapi.responses import HTMLResponse
from tools.smart_marker_injector import auto_route

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# @auto_route
@router.get("/ui_dev_reference_viewer", response_class=HTMLResponse, name="get_ui_dev_reference_viewer")
# <smart.template>
async def ui_dev_reference_viewer_page(
    request: Request,
    user=Depends(get_current_user_optional)
):
    return templates.TemplateResponse("ui_dev_reference_viewer.html", {
        "request": request,
        "user": user
    })
