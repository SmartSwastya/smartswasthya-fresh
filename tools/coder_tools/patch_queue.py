# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
import os
import json
import logging
from datetime import datetime

PATCH_QUEUE_FILE = "tools/patch_queue.json"

@auto_model
@auto_route
@auto_logic
def add_patch_instruction(patch_name: str, details: str):
    """
    Adds a new patch instruction with timestamp to the patch queue file.
    """
    patch_data = {
        "patch_name": patch_name,
        "details": details,
        "timestamp": datetime.now().isoformat()
    }

    queue = []
    if os.path.exists(PATCH_QUEUE_FILE):
        with open(PATCH_QUEUE_FILE, "r", encoding="utf-8") as f:
            try:
                queue = json.load(f)
            except json.JSONDecodeError:
                logging.warning("⚠️ Patch queue corrupted, resetting.")

    queue.append(patch_data)

    with open(PATCH_QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2)
    logging.info(f"🪛 Patch added: {patch_name}")

@auto_model
@auto_route
@auto_logic
def list_patch_queue():
    """
    Displays all scheduled patch instructions.
    """
    if not os.path.exists(PATCH_QUEUE_FILE):
        logging.info("📭 No patches in queue.")
        return []

    try:
        with open(PATCH_QUEUE_FILE, "r", encoding="utf-8") as f:
            queue = json.load(f)
            logging.info("📋 Scheduled Patch Queue:")
            for patch in queue:
                logging.info(f"🔧 {patch['patch_name']} — {patch['timestamp']}")
            return queue
    except Exception as e:
        logging.error(f"❌ Failed to read patch queue: {e}")
        return []

