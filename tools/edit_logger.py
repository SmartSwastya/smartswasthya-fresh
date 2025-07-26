# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# tools/edit_logger.py

from datetime import datetime
import os

LOG_PATH = "records/dev_logs/edit_log.txt"

@auto_model
@auto_route
@auto_logic
def log_instruction_edit(task_id: str, new_instruction: str, edited_by: str = "admin"):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {task_id} edited by {edited_by} → {new_instruction.strip()}\n"
    with open(LOG_PATH, "a", encoding="utf-8") as log_file:
        log_file.write(entry)

