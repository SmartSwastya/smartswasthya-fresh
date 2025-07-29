# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# ✅ File: scripts/manual_startup_trigger.py

import sys
from pathlib import Path

PROJECT_ROOT = str(Path(__file__).resolve().parents[2])
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from records.records import record_file_change, insert_status_history_from_file

@auto_model
@auto_route
@auto_logic
def run_startup_patch():
    model_dir = Path("models")
    for py_file in model_dir.glob("*.py"):
        if py_file.name.endswith(".bak"):
            continue
        file_path = str(py_file)
        output_path = file_path.replace("models/", "records/bak/") + ".bak"
        record_file_change(file_path, output_path)
        insert_status_history_from_file(file_path)

if __name__ == "__main__":
    run_startup_patch()

