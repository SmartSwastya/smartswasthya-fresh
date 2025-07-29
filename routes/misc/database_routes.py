# 📁 routes/dev/database_routes.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from models.backup_models import RestoreBackupRequest
from tools.smart_template import templates
from tools.obvious_router import auto_route
from handler import auto_logic, auto_model


# ╔════════════════════════════════════════════════╗
# ║ SECTION: Router Setup                          ║
# ╚════════════════════════════════════════════════╝
router = APIRouter(prefix="/dev/database", tags=["Database Manager"])


# ╔════════════════════════════════════════════════╗
# ║ SECTION: Dashboard Page                        ║
# ╚════════════════════════════════════════════════╝
@auto_route
@router.get("/", response_class=HTMLResponse)
async def database_dashboard(request: Request):
    return templates.TemplateResponse("database.html", {"request": request})


# ╔════════════════════════════════════════════════╗
# ║ SECTION: Restore API                           ║
# ╚════════════════════════════════════════════════╝
@auto_model
@auto_route
@auto_logic
@router.post("/restore", operation_id="post_backup_restore")
def restore_from_backup(payload: RestoreBackupRequest):
    ...
