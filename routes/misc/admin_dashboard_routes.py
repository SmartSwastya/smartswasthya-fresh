# ╔════════════════════════════════════════════════╗
# ║ FILE: routes/admin_dashboard_routes.py         ║
# ║ PURPOSE: Admin Dashboard route with task stats ║
# ╚════════════════════════════════════════════════╝

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from typing import Optional

from models.users import User
from models.dev_tasks import DevTask
from tools.auth import get_current_user_optional
from tools.smart_template import templates
from database import get_db
from tools.obvious_router import auto_route

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Router Setup                          ║
# ╚════════════════════════════════════════════════╝
router = APIRouter()

# ╔════════════════════════════════════════════════╗
# ║ ROUTE: Admin Dashboard                         ║
# ╚════════════════════════════════════════════════╝
@auto_route
@router.get("/admin-dashboard", response_class=HTMLResponse, name="admin-dashboard")
async def admin_dashboard(
    request: Request,
    current_user: User = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
):
    if not current_user or current_user.role != "admin":
        return templates.TemplateResponse("unauthorized.html", {"request": request})

    tasks = db.query(DevTask).all()
    total = len(tasks)
    done = sum(1 for t in tasks if t.status == "done")
    percent_complete = int((done / total) * 100) if total else 0

    return templates.TemplateResponse(
        "admin_dashboard.html",
        {
            "request": request,
            "user": current_user,
            "tasks": tasks,
            "percent_complete": percent_complete
        }
    )
