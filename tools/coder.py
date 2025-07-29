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
from pathlib import Path
from datetime import datetime

PATCH_FILE = Path(__file__).parent / "patch_queue.json"
BACKUP_DIR = Path(__file__).parent / "backup_patches"
LOG_DIR = Path(__file__).parent.parent / "records" / "patch_logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

success_entries = []
failed_entries = []

@auto_model
@auto_route
@auto_logic
def backup_original(file_path):
    rel_path = Path(file_path).relative_to(Path(__file__).parent.parent)
    backup_path = BACKUP_DIR / rel_path
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    if not backup_path.exists():
        with open(file_path, 'r', encoding='utf-8') as src, open(backup_path, 'w', encoding='utf-8') as dst:
            dst.write(src.read())

@auto_model
@auto_route
@auto_logic
def apply_patch(entry):
    base_dir = Path(__file__).parent.parent
    rel_path = Path(entry.get("file_path") or entry.get("file") or "")
    file_path = (base_dir / rel_path).resolve()

    insert_after = entry.get("insert_after")
    code_to_insert = entry.get("code")

    if not file_path or not file_path.exists():
        failed_entries.append({
            "file": str(file_path),
            "reason": "❌ File not found or path missing"
        })
        return False

    if not insert_after:
        failed_entries.append({
            "file": str(file_path),
            "reason": "❌ insert_after key missing"
        })
        return False

    if not code_to_insert:
        failed_entries.append({
            "file": str(file_path),
            "reason": "❌ code to insert missing"
        })
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        failed_entries.append({
            "file": str(file_path),
            "reason": f"❌ Failed to read: {e}"
        })
        return False

    inserted = False
    anchor_clean = insert_after.strip().lower()
    for idx, line in enumerate(lines):
        line_clean = line.strip().lower()
        if anchor_clean in line_clean:
            lines.insert(idx + 1, code_to_insert + '\n')
            inserted = True
            break

    if not inserted:
        failed_entries.append({
            "file": str(file_path),
            "reason": f"⚠️ Marker not found: {insert_after}"
        })
        return False

    try:
        backup_original(file_path)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        success_entries.append({
            "file": str(file_path),
            "insert_after": insert_after
        })
        return True
    except Exception as e:
        failed_entries.append({
            "file": str(file_path),
            "reason": f"❌ Failed to write: {e}"
        })
        return False

@auto_model
@auto_route
@auto_logic
def write_log():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    log_path = LOG_DIR / f"{timestamp}_patch_log.txt"
    with open(log_path, 'w', encoding='utf-8') as log:
        log.write(f"🛠️ Patch Run Summary — {datetime.now().strftime('%Y-%m-%d %I:%M %p')}\n\n")

        if success_entries:
            log.write("✅ SUCCESS PATCHES\n")
            for entry in success_entries:
                log.write(f" - {entry['file']} ➝ Inserted after: {entry['insert_after']}\n")
            log.write("\n")

        if failed_entries:
            log.write("❌ FAILED PATCHES\n")
            for entry in failed_entries:
                reason = entry.get("reason", "Unknown error")
                log.write(f"{reason} ➝ {entry['file']}\n")
    print(f"📄 Patch log saved: {log_path}")

@auto_model
@auto_route
@auto_logic
def apply_patch_queue():
    if not PATCH_FILE.exists():
        print("❌ patch_queue.json not found.")
        return

    with open(PATCH_FILE, 'r', encoding='utf-8') as f:
        patch_data = json.load(f)

    print(f"🔧 Total patches to apply: {len(patch_data)}")

    retained = []
    for entry in patch_data:
        if not apply_patch(entry):
            retained.append(entry)

    with open(PATCH_FILE, 'w', encoding='utf-8') as f:
        json.dump(retained, f, indent=2)

    write_log()

if __name__ == "__main__":
    print("🛠️ Starting patch process from patch_queue.json...")
    apply_patch_queue()
    print("🎉 Patch complete.")
