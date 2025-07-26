# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
import os
import tarfile
from datetime import datetime
import logging

SNAPSHOT_DIR = "tools/snapshots"

def generate_snapshot(prefix="snapshot"):
    """
    Creates a compressed tar snapshot of the current smartswasthya root directory.
    """
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_name = f"{prefix}_{timestamp}.tar.gz"
    snapshot_path = os.path.join(SNAPSHOT_DIR, snapshot_name)

    try:
        with tarfile.open(snapshot_path, "w:gz") as tar:
            tar.add("smartswasthya", arcname="smartswasthya")
        logging.info(f"📦 Snapshot created: {snapshot_path}")
    except Exception as e:
        logging.error(f"❌ Failed to create snapshot: {e}")

