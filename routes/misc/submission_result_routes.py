# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from tools.auth import get_current_user
from fastapi import Depends
from tools.smart_marker_injector import auto_route
from tools.obvious_router import auto_logic

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# @auto_route
@router.get("/submission_result", operation_id="get_submission_result", response_class=HTMLResponse)
# @auto_logic
# <smart.template>
async def submission_result(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("submission_result.html", {"request": request, "user": user})
