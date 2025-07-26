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
# ╭────────────────────────────────────────────────────────────╮
# │ 📂 LOGIC LAYER :: sync_retry_logic.py                      │
# │ Description: Handles file retry + SCP push logic           │
# ╰────────────────────────────────────────────────────────────╯

import os
import subprocess
from utils.file_scanner import should_skip_path

RETRY_LIST_PATH = "retry_list.txt"
REMOTE_SERVER = "user@ip"         # 🔐 To be replaced by env config
REMOTE_DIR = "/remote/path"

from tools.smart_logger import SmartLogger

logger = SmartLogger("SyncRetryLogic")

# @auto_logic
@auto_model
@auto_route
@auto_logic
def run(*args, **kwargs):
    logger.info("Running sync_retry_logic.run()")
    result = retry_sync_logic()
    return {
        "status": "success",
        "result": result
    }

@auto_model
@auto_route
@auto_logic
def apply(*args, **kwargs):
    logger.info("Running sync_retry_logic.apply()")
    result = retry_sync_logic()
    return {
        "status": "applied",
        "result": result
    }

# ╭────────────────────────────────────────────────────────────╮
# │ 📄 Load Retry Files                                        │
# ╰────────────────────────────────────────────────────────────╯
@auto_model
@auto_route
@auto_logic
def load_retry_files():
    if not os.path.exists(RETRY_LIST_PATH):
        return []
    with open(RETRY_LIST_PATH, "r") as f:
        return [line.strip() for line in f if line.strip()]

# ╭────────────────────────────────────────────────────────────╮
# │ 🚚 Push File via SCP                                       │
# ╰────────────────────────────────────────────────────────────╯
@auto_model
@auto_route
@auto_logic
def scp_file(file_path):
    try:
        dest = f"{REMOTE_SERVER}:{REMOTE_DIR}/"
        result = subprocess.run(["scp", file_path, dest], capture_output=True, text=True)
        return result.returncode == 0, result.stdout or result.stderr
    except Exception as e:
        return False, str(e)

# ╭────────────────────────────────────────────────────────────╮
# │ 🔁 Retry Sync Logic                                        │
# ╰────────────────────────────────────────────────────────────╯
@auto_model
@auto_route
@auto_logic
def retry_sync_logic():
    retry_files = load_retry_files()
    failed = []
    success = []

    for file_path in retry_files:
        if not os.path.exists(file_path) or should_skip_path(file_path):
            failed.append({"file": file_path, "reason": "Missing or Skipped"})
            continue

        ok, output = scp_file(file_path)
        if ok:
            success.append(file_path)
        else:
            failed.append({"file": file_path, "reason": output})

    return {"success": success, "failed": failed}

# ╭────────────────────────────────────────────────────────────╮
# │ 🧩 CLI + Route Bridge                                      │
# ╰────────────────────────────────────────────────────────────╯
@auto_model
@auto_route
@auto_logic
def retry_sync():
    result = retry_sync_logic()
    return result

