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

VERSION_LOG_PATH = "tools/version_log.json"

@auto_model
@auto_route
@auto_logic
def log_version_event(event_type: str, summary: str = ""):
    """
    Logs a version event such as build, patch, snapshot, etc.
    """
    entry = {
        "event_type": event_type,
        "summary": summary,
        "timestamp": datetime.now().isoformat()
    }

    versions = []
    if os.path.exists(VERSION_LOG_PATH):
        try:
            with open(VERSION_LOG_PATH, "r", encoding="utf-8") as f:
                versions = json.load(f)
        except json.JSONDecodeError:
            logging.warning("⚠️ version_log.json corrupted, starting fresh.")

    versions.append(entry)

    with open(VERSION_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(versions, f, indent=2)
    
    logging.info(f"📝 Version logged: {event_type} — {summary}")

@auto_model
@auto_route
@auto_logic
def list_versions():
    """
    Lists all logged version events.
    """
    if not os.path.exists(VERSION_LOG_PATH):
        logging.info("📭 No version history found.")
        return []

    try:
        with open(VERSION_LOG_PATH, "r", encoding="utf-8") as f:
            versions = json.load(f)
            logging.info("📜 Version History:")
            for v in versions:
                logging.info(f"🔹 {v['timestamp']} — {v['event_type']}: {v['summary']}")
            return versions
    except Exception as e:
        logging.error(f"❌ Failed to read version log: {e}")
        return []

