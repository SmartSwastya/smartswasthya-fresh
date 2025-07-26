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
from pathlib import Path
import threading
from tools.smart_logger import SmartLogger

logger = SmartLogger("StartupWatcher")

WATCHED_DIRS = [
    Path("smartswasthya/routes"),
    Path("smartswasthya/logic"),
    Path("smartswasthya/models"),
]

BACKUP_DIR = Path("dev_data/_autobackup")

# @auto_logic
@auto_model
@auto_route
@auto_logic
def run(*args, **kwargs):
    logger.info("Running logic: startup_watcher.run()")
    try:
        missing_dirs = [str(p) for p in WATCHED_DIRS if not p.exists()]
        if missing_dirs:
            logger.warning(f"Missing watch dirs: {missing_dirs}")
            return {"status": "warning", "missing": missing_dirs}

        logger.info("All watched directories exist.")
        return {"status": "ok", "watched": [str(p) for p in WATCHED_DIRS]}
    except Exception as e:
        logger.error(f"Run error: {e}")
        return {"status": "error", "message": str(e)}

@auto_model
@auto_route
@auto_logic
def apply(*args, **kwargs):
    logger.info("Running logic: startup_watcher.apply()")
    try:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        summary_file = BACKUP_DIR / "startup_summary.log"

        summary_content = (
            "✅ Startup watcher triggered\n"
            "✅ All directories scanned\n"
            f"🔁 Watched: {[str(p) for p in WATCHED_DIRS]}\n"
        )
        summary_file.write_text(summary_content, encoding="utf-8")

        logger.info(f"Backup summary written at {summary_file}")
        return {"status": "backed_up", "file": str(summary_file)}
    except Exception as e:
        logger.error(f"Apply error: {e}")
        return {"status": "error", "message": str(e)}

@auto_model
@auto_route
@auto_logic
def start_watcher_thread():
    @auto_model
    @auto_route
    @auto_logic
    def watch():
        logger.log_info("StartupWatcher", "Thread", "👁 Watcher thread started")
    thread = threading.Thread(target=watch, daemon=True)
    thread.start()
