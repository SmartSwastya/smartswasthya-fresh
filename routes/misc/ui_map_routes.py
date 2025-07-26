# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# 📁 routes/ui_map_routes.py

from fastapi import APIRouter, Request

from tools.obvious_router import auto_route, auto_logic
from tools.smart_template import templates

router = APIRouter(prefix="/ui-map", tags=["UI Map"])


@auto_route
@auto_logic
@router.get("")
async def map_page(request: Request):
    return templates.TemplateResponse("map.html", {"request": request})
