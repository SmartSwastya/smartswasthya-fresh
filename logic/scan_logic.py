# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_logic, auto_function
from tools.obvious_router import auto_function as obs_func
from handler import auto_logic, auto_route, auto_model

import os
from pathlib import Path
from datetime import datetime
from tools.smart_logger import SmartLogger

logger = SmartLogger("ScanLogic")
PROJECT_ROOT = Path(__file__).resolve().parent.parent

@auto_model
@auto_route
@auto_logic
def run(*args, **kwargs):
    logger.info("Running logic: scan_logic.run()")
    try:
        folders_to_check = ["routes", "models", "logic", "templates"]
        missing = []
        for folder in folders_to_check:
            path = PROJECT_ROOT / "smartswasthya" / folder
            if not path.exists():
                missing.append(folder)
        if missing:
            logger.warning(f"Missing folders: {missing}")
            return {"status": "incomplete", "missing": missing}
        logger.info("All key folders found.")
        return {"status": "ok", "checked": folders_to_check}
    except Exception as e:
        logger.error(f"Run error: {str(e)}")
        return {"status": "error", "message": str(e)}

@auto_model
@auto_route
@auto_logic
def apply(*args, **kwargs):
    logger.info("Running logic: scan_logic.apply()")
    try:
        marker_path = PROJECT_ROOT / "smartswasthya" / "templates" / ".safe_marker"
        marker_path.touch(exist_ok=True)
        logger.info(f"Safe marker created at: {marker_path}")
        return {"status": "marker_created", "path": str(marker_path)}
    except Exception as e:
        logger.error(f"Apply error: {str(e)}")
        return {"status": "error", "message": str(e)}

@auto_model
@auto_route
@auto_logic
def scan_files_between(start_time: str, end_time: str):
    logger.info(f"Scanning files modified between {start_time} and {end_time}")
    try:
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
        scanned_files = []
        target_folders = ["routes", "models", "logic", "templates"]
        for folder in target_folders:
            root_path = PROJECT_ROOT / "smartswasthya" / folder
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file():
                    continue
                mtime = datetime.fromtimestamp(path.stat().st_mtime)
                if start <= mtime <= end:
                    scanned_files.append(str(path.relative_to(PROJECT_ROOT)))
        logger.info(f"Found {len(scanned_files)} files")
        return {"status": "success", "files_found": len(scanned_files), "files": scanned_files}
    except Exception as e:
        logger.error(f"Scan error: {str(e)}")
        return {"status": "error", "message": str(e)}
