from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
"""
records.py
Location: root/smartswasthya/records/

Purpose:
1. Records every changing line.
2. Stores before and after state (brief descriptions, not full code).
3. Saves the log in a separate file for each run.
4. File name format: record_YYYY-MM-DD_HH-MM-SS.log
"""

import os
import difflib
import datetime
import re
from pathlib import Path

# PATCH START: Import SmartLogger
from tools.smart_logger import logger

# DB Models
from database import SessionLocal
from models.task_tracker.task_status_history import TaskStatusHistory
from models.task_tracker._core_base_models import TaskMaster

# Directory Config
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXCLUDE_DIRS = [".local", "node_modules", "records", "__pycache__", ".git", ".venv"]

# ========== Core File Scan Logic ==========

@auto_model
@auto_route
@auto_logic
def should_check(file_path):
    return file_path.endswith(".py") and not any(ex in file_path for ex in EXCLUDE_DIRS)

@auto_model
@auto_route
@auto_logic
def get_all_python_files():
    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            full_path = os.path.join(root, file)
            if should_check(full_path):
                yield full_path

@auto_model
@auto_route
@auto_logic
def load_file_lines(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.readlines()
    except:
        return []

try:
    from patch_reversal_engine import create_snapshot
    create_snapshot("Triggered by records.py pre-log backup")
except:
    print("[⚠️] Snapshot skipped — engine unavailable")

@auto_model
@auto_route
@auto_logic
def compare_files(old_lines, new_lines):
    diff = difflib.unified_diff(old_lines, new_lines, lineterm="", n=0)
    changes = []
    for line in diff:
        if line.startswith("+") or line.startswith("-"):
            changes.append(line)
    return changes

# def write_backup(file_path, backup_path):
#     try:
#         with open(file_path, "r", encoding="utf-8") as src, \
#              open(backup_path, "w", encoding="utf-8") as dst:
#             dst.write(src.read())
#         from tools.smart_logger import SmartLogger
#         SmartLogger("Records").log_note("Records", "Backup updated", backup_path)
#     except Exception as e:
#         print(f"[!] Failed to update backup for {file_path}: {e}")

@auto_model
@auto_route
@auto_logic
def get_log_file_path():
    log_files = sorted([
        f for f in os.listdir(os.path.dirname(__file__))
        if f.startswith("record_") and f.endswith(".log")
    ], reverse=True)

    if log_files:
        return os.path.join(os.path.dirname(__file__), log_files[0])
    else:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return os.path.join(os.path.dirname(__file__), f"record_{timestamp}.log")

# ========== Required by startup_watcher.py ==========

@auto_model
@auto_route
@auto_logic
def record_file_change(file_path: str, output_path: str):
    if not os.path.exists(file_path):
        return

    new_lines = load_file_lines(file_path)
    old_lines = load_file_lines(output_path) if os.path.exists(output_path) else []

    diff = compare_files(old_lines, new_lines)
    if diff:
        with open(get_log_file_path(), "a", encoding="utf-8") as f:
            f.write(f"\n[CHANGED] {file_path}\n")
            for line in diff:
                f.write(f"{line}\n")

    # write_backup(file_path, output_path)  # DISABLED: no .bak creation

@auto_model
@auto_route
@auto_logic
def insert_status_history_from_file(file_path: str):
    session = SessionLocal()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            match = re.match(r"^\[.*?\] Task (\d+) → (.*)$", line.strip())
            if match:
                task_id = int(match.group(1))
                status = match.group(2)
                record = TaskStatusHistory(
                    task_id=task_id,
                    status=status,
                    remarks="(auto)",
                    timestamp=datetime.datetime.now()
                )
                session.add(record)

        session.commit()
        SmartLogger("Records").log_note("Records", "Inserted task status changes from", file_path)
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        session.close()

# ========== Optional Manual Logger ==========

@auto_model
@auto_route
@auto_logic
def record_deletion(file_path: str):
    with open(get_log_file_path(), "a", encoding="utf-8") as f:
        f.write(f"\n[DELETED] File removed: {file_path}\n")

@auto_model
@auto_route
@auto_logic
def record_task_status_change(task_id: int, status: str, remarks: str = ""):
    try:
        session = SessionLocal()
        record = TaskStatusHistory(
            task_id=task_id,
            status=status,
            remarks=remarks,
            timestamp=datetime.datetime.now()
        )
        session.add(record)
        session.commit()
        print(f"[+] Task status updated: {task_id} → {status}")
    except Exception as e:
        print(f"[!] Error while recording task status: {e}")
    finally:
        session.close()

# ========== CLI Entry ==========

@auto_model
@auto_route
@auto_logic
def main():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"record_{timestamp}.log"
    log_path = os.path.join(os.path.dirname(__file__), log_filename)

    with open(log_path, "w", encoding="utf-8") as log:
        log.write(f"Change Log - {timestamp}\n")
        log.write("=" * 50 + "\n\n")

        for file_path in get_all_python_files():
            backup_path = file_path + ".bak"
            if os.path.exists(backup_path):
                old_lines = load_file_lines(backup_path)
                new_lines = load_file_lines(file_path)
                changes = compare_files(old_lines, new_lines)
                if changes:
                    log.write(f"File: {file_path}\n")
                    for change in changes:
                        log.write(f"  {change.strip()}\n")
                    log.write("\n")
                    # write_backup(file_path, backup_path)  # DISABLED: no .bak creation

# PATCH START: Logging Summary on Startup

@auto_model
@auto_route
@auto_logic
def log_summary_notes():
    logger.log_summary("Notes")
    logger.log_summary("Warnings")
    logger.log_summary("Failures")

log_summary_notes()
print("✅ log_summary_notes() called")

# PATCH END

if __name__ == "__main__":
    main()

