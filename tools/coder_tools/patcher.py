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
import shutil
import re
import logging

PATCH_QUEUE_FILE = os.path.join("tools", "patch_queue.json")
BACKUP_DIR = os.path.join("tools", "backup_files")

@auto_model
@auto_route
@auto_logic
def backup_file_if_needed(file_path):
    """Create a backup of a file if it hasn't already been backed up."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    filename = os.path.basename(file_path)
    backup_path = os.path.join(BACKUP_DIR, filename)
    if not os.path.exists(backup_path):
        shutil.copy(file_path, backup_path)
        logging.info(f"🗂️ Backup created: {backup_path}")
    else:
        logging.debug(f"⚠️ Backup already exists: {backup_path}")

@auto_model
@auto_route
@auto_logic
def apply_patch_queue():
    """Apply queued text replacements from patch_queue.json."""
    if not os.path.exists(PATCH_QUEUE_FILE):
        logging.info("✅ No patch queue found. Skipping patch step.")
        return

    try:
        with open(PATCH_QUEUE_FILE, "r", encoding="utf-8") as f:
            patch_data = json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"❌ Invalid JSON in patch_queue.json: {e}")
        return

    total_applied = 0
    for patch in patch_data.get("updates", []):
        file_path = patch.get("file")
        pattern = patch.get("pattern")
        replacement = patch.get("replacement")
        multiple = patch.get("multiple", False)

        if not (file_path and pattern is not None and replacement is not None):
            logging.warning(f"⚠️ Skipping incomplete patch entry: {patch}")
            continue

        if not os.path.exists(file_path):
            logging.warning(f"⚠️ Target file not found: {file_path}")
            continue

        backup_file_if_needed(file_path)

        with open(file_path, "r", encoding="utf-8") as f:
            original_content = f.read()

        try:
# @auto_flag: exec_eval_compile [compile]
# ⚠️ Avoid eval/exec unless sandboxed
# @auto_flag: exec_eval_compile [compile]
# ⚠️ Avoid eval/exec unless sandboxed
# @auto_flag: exec_eval_compile [compile]
# ⚠️ Avoid eval/exec unless sandboxed
            compiled_pattern = re.compile(pattern)
            new_content, count = compiled_pattern.subn(replacement, original_content, 0 if multiple else 1)
        except re.error as e:
            logging.error(f"❌ Regex error in patch: {e} for pattern {pattern}")
            continue

        if new_content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            logging.info(f"🔧 Patch applied to {file_path}: {count} replacements")
            total_applied += 1

    if total_applied:
        os.remove(PATCH_QUEUE_FILE)
        logging.info(f"✅ All patches applied. Cleared patch queue.")


