# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# File: routes/dev/dummy_routes.py

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from tools.smart_marker_injector import auto_route
from tools.obvious_router import auto_route

router = APIRouter(prefix="/dev/dummy", tags=["Dummy"])
templates = Jinja2Templates(directory="templates")

# @auto_route
@router.get("/")
@auto_model
@auto_route
@auto_logic
def dummy_page(request: Request):
    return templates.TemplateResponse("dev/dummy.html", {"request": request})
