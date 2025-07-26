# ╭──────────────────────────────────────────────────────────────╮
# │ ✅ ROUTE MODULE: sync_results_routes.py                      │
# ╰──────────────────────────────────────────────────────────────╯

# 📁 routes/dev/sync_results_routes.py

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from tools.obvious_router import auto_route, auto_logic
from tools.smart_template import templates
from tools.auth import get_current_user
from logic.sync_logic import get_synced_files

router = APIRouter()


@auto_route
@auto_logic
@router.get("/sync_results", response_class=HTMLResponse)
async def show_sync_results(request: Request, user: dict = Depends(get_current_user)):
    success, failed = get_synced_files()
    return templates.TemplateResponse("sync_results.html", {"request": request, "success": success, "failed": failed})
