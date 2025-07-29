# ╔════════════════════════════════════════════════╗
# ║ FILE: routes/dev/dev_bucket_routes.py          ║
# ║ PURPOSE: Dev Task UI & Controls                ║
# ╚════════════════════════════════════════════════╝

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import os

from tools.obvious_router import auto_route, auto_logic
from tools.auth import get_current_user
from tools.instruction_editor import edit_instruction
from tools.task_reassigner import reassign_task
from tools.json_logger import log_task_action
from database import get_db
from models.dev_tasks import DevTask

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Init                                  ║
# ╚════════════════════════════════════════════════╝
router = APIRouter(prefix="/dev-bucket", tags=["Dev Bucket"])
templates = Jinja2Templates(directory="templates")
LOG_PATH = "records/dev_logs/reassign_log.txt"

# ╔════════════════════════════════════════════════╗
# ║ ROUTE: Dev Bucket UI                           ║
# ╚════════════════════════════════════════════════╝
@auto_route
@auto_logic
@router.get("/ui", operation_id="get_ui", response_class=HTMLResponse)
async def render_dev_bucket_ui(
    request: Request,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(DevTask)
    if status:
        query = query.filter(DevTask.status == status)
    if priority:
        query = query.filter(DevTask.priority == priority)
    tasks = query.order_by(DevTask.created_at.desc()).all()

    return templates.TemplateResponse("dev_bucket.html", {
        "request": request,
        "tasks": tasks
    })

# ╔════════════════════════════════════════════════╗
# ║ ROUTE: Update Task Status                      ║
# ╚════════════════════════════════════════════════╝
@auto_route
@auto_logic
@router.post("/status/{task_id}", operation_id="post_status_{task_id}")
async def update_task_status(task_id: str, status: str = Form(...), db: Session = Depends(get_db)):
    task = db.query(DevTask).filter(DevTask.task_id == task_id).first()
    if task:
        task.status = status
        task.updated_at = datetime.utcnow()
        db.commit()
        log_task_action(task_id=task.task_id, action="status_update", new_status=status)
    return RedirectResponse(url="/dev-bucket/ui", status_code=303)

# ╔════════════════════════════════════════════════╗
# ║ ROUTE: Edit Task Instructions                  ║
# ╚════════════════════════════════════════════════╝
@auto_route
@auto_logic
@router.get("/edit/{task_id}", operation_id="get_edit_{task_id}", response_class=HTMLResponse)
async def edit_task_view(request: Request, task_id: str, db: Session = Depends(get_db)):
    task = db.query(DevTask).filter(DevTask.task_id == task_id).first()
    if not task:
        return HTMLResponse("Task not found", status_code=404)
    return templates.TemplateResponse("edit_task.html", {
        "request": request,
        "task": task
    })

@auto_route
@auto_logic
@router.post("/edit/{task_id}", operation_id="post_edit_{task_id}")
async def edit_task_submit(task_id: str, updated_instruction: str = Form(...)):
    edit_instruction(task_id, updated_instruction)
    return RedirectResponse(url="/dev-bucket/ui", status_code=303)

# ╔════════════════════════════════════════════════╗
# ║ ROUTE: Reassign Task                           ║
# ╚════════════════════════════════════════════════╝
@auto_route
@auto_logic
@router.post("/reassign/{task_id}", operation_id="post_reassign_{task_id}")
async def reassign_task_post(task_id: str, new_dev: str = Form(...)):
    reassign_task(task_id, new_dev)
    return RedirectResponse(url="/dev-bucket/ui", status_code=303)

# ╔════════════════════════════════════════════════╗
# ║ ROUTE: Hold & Unhold Task                      ║
# ╚════════════════════════════════════════════════╝
@auto_route
@auto_logic
@router.post("/hold/{task_id}", operation_id="post_hold_{task_id}")
async def hold_task(task_id: str, reason: str = Form(default="No reason"), db: Session = Depends(get_db)):
    task = db.query(DevTask).filter(DevTask.task_id == task_id).first()
    if task:
        task.status = "hold"
        task.admin_remarks = reason
        task.updated_at = datetime.utcnow()
        db.commit()
    return RedirectResponse(url="/dev-bucket/ui", status_code=303)

@auto_route
@auto_logic
@router.post("/unhold/{task_id}", operation_id="post_unhold_{task_id}")
async def unhold_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(DevTask).filter(DevTask.task_id == task_id).first()
    if task and task.status == "hold":
        task.status = "new"
        task.updated_at = datetime.utcnow()
        db.commit()
    return RedirectResponse(url="/dev-bucket/ui", status_code=303)

# ╔════════════════════════════════════════════════╗
# ║ ROUTE: View / Download Logs                    ║
# ╚════════════════════════════════════════════════╝
@auto_route
@auto_logic
@router.get("/logs/reassign", operation_id="get_logs_reassign", response_class=PlainTextResponse)
async def view_reassign_log():
    if not os.path.exists(LOG_PATH):
        return PlainTextResponse("[📭] No reassign log found yet.", status_code=200)
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        return f.read()

@auto_route
@auto_logic
@router.get("/logs/reassign/download", operation_id="get_logs_reassign_download")
async def download_reassign_log():
    if not os.path.exists(LOG_PATH):
        return PlainTextResponse("[❌] Log file not found", status_code=404)
    return FileResponse(LOG_PATH, filename="reassign_log.txt", media_type="text/plain")
