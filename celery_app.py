# ╔════════════════════════════════════════════════════╗
# ║              CELERY APP INITIALIZATION            ║
# ╚════════════════════════════════════════════════════╝

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
import os
from dotenv import load_dotenv
from celery import Celery
from tools.smart_logger import SmartLogger

# 📥 Load environment variables
load_dotenv()

# 🔐 Fail-safe: Check broker and backend environment variables
broker_url = os.getenv("CELERY_BROKER_URL")
if not broker_url:
    raise EnvironmentError("❌ Missing CELERY_BROKER_URL in environment")

result_backend = os.getenv("CELERY_RESULT_BACKEND")
if not result_backend:
    raise EnvironmentError("❌ Missing CELERY_RESULT_BACKEND in environment")

# 🚀 Celery App Instance
celery_app = Celery("smartworker", broker=broker_url, backend=result_backend)

# 📋 Initialize logger
logger = SmartLogger("CeleryInit")
logger.log_info("Celery", "Startup", "🚀 Celery worker initialized.")

# ⏲️ Load beat schedule
from celery_beat_schedule import beat_schedule_config
celery_app.conf.beat_schedule = beat_schedule_config
celery_app.conf.timezone = "Asia/Kolkata"

# 🔍 Auto-discover tasks from the 'tasks' package
celery_app.autodiscover_tasks(["tasks"])

# ⚙️ Task Routing & Configs
celery_app.conf.task_routes = {
    "tasks.cleanup_old_files": {"queue": "default"},
}

celery_app.conf.update(
    task_track_started=True,
    task_time_limit=300,
    broker_connection_retry_on_startup=True
)

# ✅ Optional preload (safe to keep, remove if modularizing later)
try:
    import tasks.cleanup_task
except ImportError:
    print("⚠️ Optional preload 'cleanup_task' not found. Skipped.")

