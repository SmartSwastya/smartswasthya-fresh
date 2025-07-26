# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# 🔁 PATCH ROLLBACK MANAGER
# 📁 File: tools/rollback_manager.py
# 🎯 Purpose: Capture and restore snapshots before patch overwrite
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

import os
import shutil
from datetime import datetime
from pathlib import Path

REVISION_DIR = Path("revisions")

@auto_model
@auto_route
@auto_logic
def snapshot_files(file_list, patch_id):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = REVISION_DIR / patch_id / timestamp
    os.makedirs(backup_path, exist_ok=True)

    for file in file_list:
        try:
            file_path = Path(file)
            if file_path.exists():
                dest_path = backup_path / file_path.name
                shutil.copy2(file_path, dest_path)
                print(f"✅ Backed up: {file} → {dest_path}")
            else:
                print(f"⚠️ File not found: {file}")
        except Exception as e:
            print(f"❌ Error copying {file}: {e}")

@auto_model
@auto_route
@auto_logic
def restore_patch_snapshot(patch_id, timestamp):
    snapshot_path = REVISION_DIR / patch_id / timestamp
    if not snapshot_path.exists():
        print("❌ Snapshot not found.")
        return

    for file in snapshot_path.iterdir():
        try:
            target = Path("smartswasthya") / file.name
            shutil.copy2(file, target)
            print(f"🛠️ Restored: {file.name}")
        except Exception as e:
            print(f"❌ Restore failed for {file.name}: {e}")

# 🧪 Example Usage:
if __name__ == "__main__":
    sample_files = ["main.py", "logic/startup_watcher.py"]
    snapshot_files(sample_files, patch_id="TASK_102")
    # restore_patch_snapshot("TASK_102", "20250614_211502")

