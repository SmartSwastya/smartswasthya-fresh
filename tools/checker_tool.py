# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# ╔════════════════════════════════════════════════════════════════════╗
# ║       SMART SWASTHYA – LOGIC CHECKER TOOL (live v4 optimized)     ║
# ║   Compares live v4 folder with v1 TAR archive for diff mapping    ║
# ╚════════════════════════════════════════════════════════════════════╝

import os
import shutil
import json
from utils.file_scanner import list_all_files, extract_tar_file

# ✅ Live v4 folder (no more extraction needed)
CURRENT_DIR = "/mnt/data/root/smartswasthya"

# 🕰️ Previous version (v1 TAR)
PREVIOUS_DIR = "/mnt/data/previous_scan"

@auto_model
@auto_route
@auto_logic
def setup_temp_dirs():
    # 🧹 Clean only previous version scan folder
    if os.path.exists(PREVIOUS_DIR):
        shutil.rmtree(PREVIOUS_DIR)
    os.makedirs(PREVIOUS_DIR)

@auto_model
@auto_route
@auto_logic
def extract_all():
    print("📦 Extracting V1 TAR...")
    extract_tar_file(
        "/mnt/data/smartswasthya/tools/checker/previous_version/smartswasthya_full.tar",
        PREVIOUS_DIR
    )

@auto_model
@auto_route
@auto_logic
def compare_python_files():
    print("🔎 Comparing .py files in current vs previous version...")

    current_files = list_all_files(os.path.join(CURRENT_DIR, "smartswasthya"))
    previous_files = list_all_files(os.path.join(PREVIOUS_DIR, "smartswasthya"))

    current_set = set(os.path.relpath(f, os.path.join(CURRENT_DIR, "smartswasthya")) for f in current_files)
    previous_set = set(os.path.relpath(f, os.path.join(PREVIOUS_DIR, "smartswasthya")) for f in previous_files)

    added = sorted(list(current_set - previous_set))
    removed = sorted(list(previous_set - current_set))
    common = sorted(list(current_set & previous_set))

    print(f"🟢 Added: {len(added)}")
    print(f"🔴 Removed: {len(removed)}")
    print(f"🟡 Common: {len(common)}")

    return {"added": added, "removed": removed, "common": common}

@auto_model
@auto_route
@auto_logic
def run_checker():
    print("🚀 Checker Tool Starting...")
    setup_temp_dirs()
    extract_all()
    changes = compare_python_files()

    with open("/mnt/data/logic_diff_summary.json", "w") as f:
        json.dump(changes, f, indent=2)

    print("✅ Summary saved: logic_diff_summary.json")

if __name__ == "__main__":
    run_checker()

