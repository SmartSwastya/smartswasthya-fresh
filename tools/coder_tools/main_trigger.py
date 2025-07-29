# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
import sys
from coder_tools.patcher import apply_patch_queue
from coder_tools.duplicator import handle_route_duplicates
from coder_tools.dummy_checker import log_dummy_outputs
from coder_tools.pyproject_writer import generate_pyproject_if_missing
from coder_tools.snapshot_generator import generate_snapshot
from coder_tools.docs_sync import sync_developer_docs
from coder_tools.patch_queue import add_patch_instruction, list_patch_queue
from coder_tools.route_conflict_handler import detect_route_conflicts
from coder_tools.version_tracker import log_version_event, list_versions

MENU = {
    "1": ("Apply Patch Queue", apply_patch_queue),
    "2": ("Handle Route Duplicates", handle_route_duplicates),
    "3": ("Log Dummy/Placeholder Code", log_dummy_outputs),
    "4": ("Generate pyproject.toml if Missing", generate_pyproject_if_missing),
    "5": ("Generate Project Snapshot", generate_snapshot),
    "6": ("Sync Developer Docs", sync_developer_docs),
    "7": {
        "title": "Patch Queue Manager",
        "sub": {
            "1": ("Add Patch Instruction", add_patch_instruction),
            "2": ("List Patch Queue", list_patch_queue),
        }
    },
    "8": ("Detect Route Conflicts", detect_route_conflicts),
    "9": {
        "title": "Version Tracker",
        "sub": {
            "1": ("Log Version Event", lambda: log_version_event("manual", "Manual trigger")),
            "2": ("List Version History", list_versions),
        }
    },
    "0": ("Exit", sys.exit)
}

@auto_model
@auto_route
@auto_logic
def print_menu(menu):
    print("\n🔧 Coder Tools Menu:")
    for key, value in menu.items():
        if isinstance(value, dict):
            print(f" {key}. {value['title']} ➤")
        else:
            print(f" {key}. {value[0]}")

@auto_model
@auto_route
@auto_logic
def main():
    while True:
        print_menu(MENU)
# @auto_flag: input_shell [input(]
# ⚠️ input() or shell call found — sanitize required
# @auto_flag: input_shell [input(]
# ⚠️ input() or shell call found — sanitize required
# @auto_flag: input_shell [input(]
# ⚠️ input() or shell call found — sanitize required
        choice = input("🔸 Select an option: ").strip()

        if choice not in MENU:
            print("❌ Invalid option. Try again.")
            continue

        item = MENU[choice]
        if isinstance(item, tuple):
            print(f"⚙️ Running: {item[0]}")
            item[1]()
        elif isinstance(item, dict):
            while True:
                print(f"\n🔸 {item['title']} Submenu:")
                for sub_key, (sub_title, _) in item['sub'].items():
                    print(f"   {sub_key}. {sub_title}")
                print("   0. Back to Main Menu")
                sub_choice = input("   ➤ Choose: ").strip()
                if sub_choice == "0":
                    break
                if sub_choice not in item['sub']:
                    print("   ❌ Invalid sub-option.")
                    continue
                print(f"   ⚙️ Running: {item['sub'][sub_choice][0]}")
                item['sub'][sub_choice][1]()

if __name__ == "__main__":
    main()

