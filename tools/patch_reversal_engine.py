# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
"""
patch_reversal_engine.py

Unified engine to manage:
1. 🧠 .bak based single-file patch reversals (reversal_registry.json)
2. 🗂️ Full project snapshots with optional notes (patch_snapshots/)

CLI Usage:
    python tools/patch_reversal_engine.py --snapshot --note "Before major patch"
    python tools/patch_reversal_engine.py --restore-snapshot snapshot_YYYY-MM-DD_HH-MM-SS
    python tools/patch_reversal_engine.py --scan-backups
    python tools/patch_reversal_engine.py --reverse-all
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path
from typing import Dict
import argparse

from tools.smart_logger import SmartLogger

# === Common Paths ===
BASE_DIR = Path(__file__).resolve().parent.parent
TARGET_DIR = BASE_DIR / "smartswasthya"
SNAPSHOT_DIR = TARGET_DIR / "patch_snapshots"
REVERSAL_REGISTRY_FILE = BASE_DIR / "registry" / "reversal_registry.json"
BACKUP_SUFFIX = ".bak"

logger = SmartLogger("PatchReversal")

# === SNAPSHOT SYSTEM ===

@auto_model
@auto_route
@auto_logic
def create_snapshot(note: str = ""):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    snapshot_path = SNAPSHOT_DIR / f"snapshot_{timestamp}"
    snapshot_path.mkdir(parents=True, exist_ok=True)

    for file in TARGET_DIR.rglob("*.py"):
        rel_path = file.relative_to(TARGET_DIR)
        dest = snapshot_path / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file, dest)

    if note:
        with open(snapshot_path / "note.txt", "w", encoding="utf-8") as f:
            f.write(note)

    logger.log_success("Snapshot", "Created", str(snapshot_path))

@auto_model
@auto_route
@auto_logic
def list_snapshots():
    if not SNAPSHOT_DIR.exists():
        return []
    return sorted([p for p in SNAPSHOT_DIR.iterdir() if p.is_dir()], reverse=True)

@auto_model
@auto_route
@auto_logic
def restore_snapshot(snapshot_name: str):
    snapshot_folder = SNAPSHOT_DIR / snapshot_name
    if not snapshot_folder.exists():
        raise FileNotFoundError(f"Snapshot folder not found: {snapshot_folder}")

    for file in snapshot_folder.rglob("*.py"):
        rel_path = file.relative_to(snapshot_folder)
        dest = TARGET_DIR / rel_path
        shutil.copy2(file, dest)

    logger.log_success("Snapshot", "Restored", snapshot_name)

# === REVERSAL REGISTRY SYSTEM ===

@auto_model
@auto_route
@auto_logic
def find_patched_files(directory: Path, suffix=BACKUP_SUFFIX) -> Dict[str, str]:
    registry = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(suffix):
                original = file[:-len(suffix)]
                original_path = Path(root) / original
                backup_path = Path(root) / file
                if original_path.exists():
                    registry[str(original_path.relative_to(BASE_DIR))] = str(backup_path.relative_to(BASE_DIR))
    return registry

@auto_model
@auto_route
@auto_logic
def save_registry(registry: Dict[str, str]):
    REVERSAL_REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REVERSAL_REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)
    logger.log_success("Reversal Engine", "Saved", f"{len(registry)} entries in reversal_registry.json")

@auto_model
@auto_route
@auto_logic
def reverse_patch(file_path: str):
    abs_file = BASE_DIR / file_path
    bak_file = BASE_DIR / (file_path + BACKUP_SUFFIX)

    if not bak_file.exists():
        logger.log_warning("Reversal", "Backup Missing", file_path)
        return

    with open(bak_file, "r", encoding="utf-8") as f:
        content = f.read()

    with open(abs_file, "w", encoding="utf-8") as f:
        f.write(content)

    logger.log_success("Reversal", "Reversed", file_path)

@auto_model
@auto_route
@auto_logic
def reverse_all():
    if not REVERSAL_REGISTRY_FILE.exists():
        logger.log_warning("Reversal", "No Registry", "reversal_registry.json not found")
        return
    with open(REVERSAL_REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)
    for file_path in registry:
        reverse_patch(file_path)

@auto_model
@auto_route
@auto_logic
def show_patch_summary():
    if not REVERSAL_REGISTRY_FILE.exists():
        print("No reversal registry available.")
        return
    with open(REVERSAL_REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)
    print(f"🔁 Reversal-ready files: {len(registry)}")
    for k, v in registry.items():
        print(f"→ {k} can be restored from {v}")

# === CLI ENTRY ===

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Patch Reversal Engine (Snapshot + Reversal)")
    parser.add_argument("--snapshot", action="store_true", help="Create snapshot of all .py files")
    parser.add_argument("--note", type=str, default="", help="Optional note for snapshot")
    parser.add_argument("--restore-snapshot", type=str, help="Snapshot folder name to restore")
    parser.add_argument("--scan-backups", action="store_true", help="Scan for .bak files and update reversal registry")
    parser.add_argument("--reverse-all", action="store_true", help="Reverse all files listed in reversal_registry.json")

    args = parser.parse_args()

    if args.snapshot:
        create_snapshot(args.note)
    elif args.restore_snapshot:
        restore_snapshot(args.restore_snapshot)
    elif args.scan_backups:
        reversal_map = find_patched_files(BASE_DIR)
        save_registry(reversal_map)
        show_patch_summary()
    elif args.reverse_all:
        reverse_all()
    else:
        print("\n📂 Available Snapshots:")
        for snap in list_snapshots():
            print(" -", snap.name)
        print("\n📦 To scan .bak files, run with --scan-backups")

