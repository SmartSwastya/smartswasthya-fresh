# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_route
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_route
from tools.obvious_router import auto_function
# @auto_function
# 📁 routes/dev_dashboard_routes.py

from fastapi import APIRouter, Request, Depends  # ✅ FIXED
from fastapi.responses import JSONResponse
from handler import auto_logic, auto_route, auto_model
from models.dev_tasks import DevTask
from sqlalchemy.orm import Session
from database import get_db
from tools.auth import get_current_user_optional
from tools.smart_template import templates
from models.users import User

router = APIRouter()

# @auto_route
@router.get("/dev-dashboard")
# <smart.template>
@auto_model
@auto_route
@auto_logic
def dev_dashboard_view(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    try:
        tasks = db.query(DevTask).all()
        done = len([t for t in tasks if t.status == "done"])
        percent_complete = int((done / len(tasks)) * 100) if tasks else 0

        return templates.TemplateResponse("dev_dashboard.html", {
            "request": request,
            "tasks": tasks,
            "percent_complete": percent_complete,
            "email": current_user.email if current_user else "Anonymous"
        })

    except Exception as e:
        print(f"🔥 Error loading /dev-dashboard: {str(e)}")
        return JSONResponse(status_code=500, content={"status": "fail", "message": "Internal Error"})
