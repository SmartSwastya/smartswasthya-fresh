# 📁 routes/console_dashboard_routes.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from tools.obvious_router import auto_route, auto_logic
from tools.smart_template import templates
from tools.auth import get_current_user

from logic.scan_logic import scan_files_between
from logic.sync_retry_logic import retry_sync


# ╔════════════════════════════════════════════════╗
# ║ SECTION: Router Setup                          ║
# ╚════════════════════════════════════════════════╝
router = APIRouter()


# ╔════════════════════════════════════════════════╗
# ║ SECTION: Console Dashboard                     ║
# ╚════════════════════════════════════════════════╝
@auto_route
@auto_logic
@router.get("/console_dashboard", response_class=HTMLResponse, operation_id="get_console_dashboard")
async def dashboard_page(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("console.html", {"request": request, "current_user": user})

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Scan Operation                        ║
# ╚════════════════════════════════════════════════╝
@auto_route
@auto_logic
@router.post("/scan", operation_id="post_scan")
async def handle_scan(request: Request, start: str = Form(...), end: str = Form(...)):
    scan_files_between(start, end)
    return RedirectResponse("/scan_results", status_code=303)


# ╔════════════════════════════════════════════════╗
# ║ SECTION: Sync Operation                        ║
# ╚════════════════════════════════════════════════╝
@auto_route
@auto_logic
@router.post("/sync", operation_id="post_sync")
async def handle_sync():
    retry_sync()
    return RedirectResponse("/sync_results", status_code=303)
