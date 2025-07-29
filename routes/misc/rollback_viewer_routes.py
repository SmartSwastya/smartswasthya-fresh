# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.obvious_router import auto_logic
#region auto_route
# ======================================
# 📁 FILE: routes/rollback_viewer_routes.py
# 🎯 PURPOSE: Display all patch snapshots stored
# ======================================

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pathlib import Path
import json
from datetime import datetime
from fastapi.templating import Jinja2Templates
from tools.auth import get_current_user
from fastapi import Depends
from tools.smart_marker_injector import auto_route

router = APIRouter(
    prefix="/rollback",
    tags=["rollback"]
)
templates = Jinja2Templates(directory="templates")

# @auto_route
@router.get("/rollback-viewer", operation_id="get_rollback-viewer", response_class=HTMLResponse)
# @auto_logic
# <smart.template>
async def view_snapshots(request: Request, user: dict = Depends(get_current_user)):
    snapshot_dir = Path("snapshots/")
    rollback_data = []

    if snapshot_dir.exists():
        for folder in sorted(snapshot_dir.iterdir(), reverse=True):
            if folder.is_dir():
                patch_id = folder.name
                files = [str(f.name) for f in folder.glob("*")]
                timestamp = datetime.fromtimestamp(folder.stat().st_ctime).strftime("%Y-%m-%d %H:%M:%S")
                rollback_data.append({
                    "patch_id": patch_id,
                    "files": files,
                    "timestamp": timestamp
                })

    return templates.TemplateResponse("rollback_viewer.html", {
        "request": request,
        "rollback_data": rollback_data
    })
