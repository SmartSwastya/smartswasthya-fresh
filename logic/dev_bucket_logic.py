# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_logic
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from tools.obvious_router import auto_logic
from handler import auto_logic
from handler import auto_route
from handler import auto_model
#region auto_logic
# ===============================
# 📁 FILE: logic/dev_bucket_logic.py
# 📌 Purpose: Handle task fetching, details, submission for Dev Bucket
# ===============================
import os
import sys
import json
from pathlib import Path
from datetime import datetime

from tools.rollback_manager import snapshot_files
from celery_app import celery_app
from tools.smart_logger import SmartLogger

# 🌐 Path Standardization
PROJECT_ROOT = str(Path(__file__).resolve().parents[1])
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# 📍 Logger Setup
logger = SmartLogger("DevBucketLogic")

# 📁 Static JSON Paths
DEV_BUCKET_JSON = Path(PROJECT_ROOT) / "dev_data" / "tasks.json"
SUBMISSION_LOG_JSON = Path(PROJECT_ROOT) / "dev_data" / "dev_bucket_submissions.json"

# ===============================
# 🔹 Runner Function (Dev only)
# ===============================
# @auto_logic
@auto_model
@auto_route
@auto_logic
def run():
    logger.info("Running logic: dev_bucket_logic.run()")
    try:
        user = {"email": "date.hrushikesh@gmail.com"}
        tasks = fetch_all_tasks(user)
        logger.info(f"Tasks fetched: {len(tasks)}")
        return {"status": "success", "task_count": len(tasks)}
    except Exception as e:
        logger.error(f"Run error: {str(e)}")
        return {"status": "error", "message": str(e)}

@auto_model
@auto_route
@auto_logic
def apply():
    logger.info("Running logic: dev_bucket_logic.apply()")
    try:
        task_id = "TEST123"
        user_email = "date.hrushikesh@gmail.com"
        comments = "Auto-test submission from apply()"
        result = submit_task_result(task_id, user_email, comments)
        logger.info("Submission simulated.")
        return {"status": "applied", "log": result}
    except Exception as e:
        logger.error(f"Apply error: {str(e)}")
        return {"status": "error", "message": str(e)}

# ===============================
# 📌 Function: Fetch All Tasks
# ===============================
@auto_model
@auto_route
@auto_logic
def fetch_all_tasks(user):
    logger.info(f"📥 Incoming user: {user}")
    logger.info(f"📁 Task JSON path: {DEV_BUCKET_JSON}")

    if not DEV_BUCKET_JSON.exists():
        logger.warning("❌ Task file not found.")
        return []

    with open(DEV_BUCKET_JSON, "r", encoding="utf-8") as f:
        all_tasks = json.load(f)

    user_email = user.get("email", "")
    if user_email in ["date.hrushikesh@gmail.com", "vkota2774@gmail.com"]:
        logger.info("✅ Super Admin Mode — Returning all tasks.")
        return all_tasks

    user_tasks = [task for task in all_tasks if task.get("assigned_to") == user_email]
    logger.info(f"🧠 Filtered tasks for {user_email}: {len(user_tasks)}")
    return user_tasks

# ===============================
# 📌 Function: Get Task Details
# ===============================
@auto_model
@auto_route
@auto_logic
def get_task_details(task_id):
    if not DEV_BUCKET_JSON.exists():
        logger.warning("❌ Task file not found.")
        return {}

    with open(DEV_BUCKET_JSON, "r", encoding="utf-8") as f:
        all_tasks = json.load(f)

    for task in all_tasks:
        if task.get("task_id") == task_id:
            logger.info(f"✅ Task found: {task_id}")
            return task

    logger.warning(f"❌ Task not found: {task_id}")
    return {}

# ===============================
# 📌 Function: Submit Task Result
# ===============================
@auto_model
@auto_route
@auto_logic
def submit_task_result(task_id, user_email, comments, touched_files=None):
    if touched_files:
        logger.info("🔁 Taking snapshot of modified files...")
        snapshot_files(task_id, touched_files)

    log_entry = {
        "task_id": task_id,
        "submitted_by": user_email,
        "comments": comments,
        "timestamp": datetime.utcnow().isoformat()
    }

    existing_logs = []
    if SUBMISSION_LOG_JSON.exists():
        with open(SUBMISSION_LOG_JSON, "r", encoding="utf-8") as f:
            existing_logs = json.load(f)

    existing_logs.append(log_entry)

    with open(SUBMISSION_LOG_JSON, "w", encoding="utf-8") as f:
        json.dump(existing_logs, f, indent=2)

    logger.info(f"✅ Submission logged for task {task_id}")
    return log_entry

