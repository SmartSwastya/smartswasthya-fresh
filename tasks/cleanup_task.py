# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# ╔════════════════════════════════════════════════════╗
# ║        SYS003 – AUTO CLEANUP SYSTEM TASK          ║
# ╚════════════════════════════════════════════════════╝

from celery import shared_task
import os
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # Ensure .env is loaded

@shared_task
@auto_model
@auto_route
@auto_logic
def cleanup_old_files():
    print("🧹 Auto Cleanup started...")

    cleanup_dirs = ["/tmp", "uploads/temp"]
    cleanup_days = int(os.getenv("CLEANUP_DAYS", 2))
    now = time.time()
    cutoff_time = now - (cleanup_days * 86400)

    deleted_files = []
    for base_dir in cleanup_dirs:
        if not os.path.exists(base_dir):
            continue
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    if os.path.getmtime(file_path) < cutoff_time:
                        os.remove(file_path)
                        deleted_files.append(file_path)
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

    log_line = f"[{datetime.now()}] Deleted {len(deleted_files)} files:\n" + "\n".join(deleted_files) + "\n\n"
    os.makedirs("log", exist_ok=True)
    with open("log/cleanup.log", "a") as log_file:
        log_file.write(log_line)

    print("✅ Auto Cleanup completed.")
    return {"deleted_count": len(deleted_files), "details": deleted_files}

