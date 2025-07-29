# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
import os
import shutil
import logging
from datetime import datetime

SOURCE_DOCS_DIR = "developer_docs"
TARGET_DOCS_DIR = "smartswasthya/docs"
VERSIONED_LOG_DIR = "smartswasthya/docs/history"

def sync_developer_docs():
    """
    Syncs markdown-based developer docs into the main project docs folder.
    """
    if not os.path.exists(SOURCE_DOCS_DIR):
        logging.warning("📁 No developer_docs directory found.")
        return

    os.makedirs(TARGET_DOCS_DIR, exist_ok=True)
    os.makedirs(VERSIONED_LOG_DIR, exist_ok=True)

    for filename in os.listdir(SOURCE_DOCS_DIR):
        if filename.endswith(".md"):
            src_path = os.path.join(SOURCE_DOCS_DIR, filename)
            target_path = os.path.join(TARGET_DOCS_DIR, filename)

            try:
                shutil.copy2(src_path, target_path)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                versioned = os.path.join(VERSIONED_LOG_DIR, f"{filename}_{timestamp}")
                shutil.copy2(src_path, versioned)
                logging.info(f"📄 Synced {filename} → docs and versioned.")
            except Exception as e:
                logging.error(f"❌ Error copying {filename}: {e}")

