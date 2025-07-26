# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_logger import SmartLogger
from tools.smart_marker_injector import auto_logic, auto_function
from tools.obvious_router import auto_function as obs_func
from handler import auto_logic, auto_route, auto_model

from pathlib import Path
import json
from datetime import datetime

logger = SmartLogger("SyncLogic")
SYNC_LOG = Path("records/sync_log.json")

@auto_model
@auto_route
@auto_logic
def run(*args, **kwargs):
    logger.info("Running sync_logic.run()")
    try:
        result = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "synced": ["routes/core/login_routes.py", "routes/misc/env_routes.py"]
        }
        _log_sync(result)
        logger.success("Sync completed.")
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"Sync run failed: {str(e)}")
        return {"status": "error", "message": str(e)}

@auto_model
@auto_route
@auto_logic
def apply(*args, **kwargs):
    logger.info("Running sync_logic.apply()")
    try:
        updated_files = ["logic/sync_logic.py", "routes/tools/sync_routes.py"]
        result = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "updated": updated_files
        }
        _log_sync(result)
        logger.info(f"Files marked as updated: {updated_files}")
        return {"status": "applied", "details": result}
    except Exception as e:
        logger.error(f"Apply failed: {str(e)}")
        return {"status": "error", "message": str(e)}

@auto_model
@auto_route
@auto_logic
def get_synced_files():
    logger.info("Fetching list of previously synced files...")
    try:
        if not SYNC_LOG.exists():
            return {"status": "ok", "files": [], "log": []}
        content = json.loads(SYNC_LOG.read_text())
        flat_files = sorted({f for entry in content for f in entry.get("synced", []) + entry.get("updated", [])})
        return {"status": "ok", "files": flat_files, "log": content}
    except Exception as e:
        logger.error(f"Fetch failed: {str(e)}")
        return {"status": "error", "message": str(e)}

def _log_sync(entry: dict):
    try:
        SYNC_LOG.parent.mkdir(parents=True, exist_ok=True)
        if SYNC_LOG.exists():
            content = json.loads(SYNC_LOG.read_text())
        else:
            content = []
        content.append(entry)
        SYNC_LOG.write_text(json.dumps(content, indent=2))
        logger.debug("Sync log updated.")
    except Exception as e:
        logger.warning(f"Log write failed: {str(e)}")
