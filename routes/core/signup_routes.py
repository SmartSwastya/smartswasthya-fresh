# ╔════════════════════════════════════════════════╗
# ║ FILE: routes/signup_routes.py                  ║
# ║ PURPOSE: Signup page + invite status API       ║
# ╚════════════════════════════════════════════════╝

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from pydantic import BaseModel

from tools.auth import get_current_user_optional
from tools.smart_marker_injector import auto_route
from handler import auto_logic, auto_model
from tools.smart_template import templates

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Router Init                           ║
# ╚════════════════════════════════════════════════╝
router = APIRouter()

# ╔════════════════════════════════════════════════╗
# ║ SECTION: UI Route                              ║
# ╚════════════════════════════════════════════════╝
@auto_route
@router.get("/signup", response_class=HTMLResponse)
@auto_logic
async def show_signup_page(request: Request, user: Optional[dict] = Depends(get_current_user_optional)):
    return templates.TemplateResponse("signup.html", {
        "request": request,
        "user": user
    })


# ╔════════════════════════════════════════════════╗
# ║ SECTION: Invite Check API                      ║
# ╚════════════════════════════════════════════════╝
class InviteStatusRequest(BaseModel):
    email: str

@auto_route
@router.post("/check_invite_status", operation_id="post_check_invite_status")
@auto_model
@auto_logic
def check_invite_status(payload: InviteStatusRequest):
    # TODO: Implement logic to check if email is invited
    return {"status": "ok", "message": "Stub: invite status checked"}
