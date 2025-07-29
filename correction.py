# 🔧 Smart Correction Engine — Refactored Fix
# 📍 Location: root/smartswasthya/correction.py
# 🧘 Philosophy: No assumptions, Pure verification

import os
import json
import re
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SUSPICIOUS_REPORT = os.path.join(PROJECT_ROOT, 'records', 'suspicious_code_report.json')
USAGE_MAP_PATH = os.path.join(PROJECT_ROOT, 'function_usage_map.json')
LOG_DIR = os.path.join(PROJECT_ROOT, 'correction_logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, f"smart_correction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

IGNORE_FOLDERS = {'__pycache__', '.git', '.idea', '.vscode', 'records', 'logs'}

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def write_log(entry: str):
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(entry + '\n')
    print(entry)

def find_py_files(root):
    py_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_FOLDERS]
        for file in filenames:
            if file.endswith('.py'):
                py_files.append(os.path.join(dirpath, file))
    return py_files

def suggest_fix(item_type, match):
    return {
        "dangerous_imports":      f"# ⚠️ Suspicious import: `{match}` — review or isolate",
# @auto_flag: input_shell [input(]
# ⚠️ input() or shell call found — sanitize required
        "input_shell":            "# ⚠️ input() or shell call found — sanitize required",
        "script_tags":            "# ⚠️ HTML script tag used — validate client-side security",
        "dynamic_imports":        "# ⚠️ Dynamic import detected — avoid in core logic",
        "hardcoded_secrets":      "# ⚠️ Hardcoded secret? Move to environment config",
        "exec_eval_compile":      "# ⚠️ Avoid eval/exec unless sandboxed",
        "encoded_blobs":          "# ⚠️ Encoded binary/blob found — verify authenticity"
    }.get(item_type, f"# ⚠️ Check for: {match}")

def run_correction():
    write_log("🔧 Smart Correction Engine Started...")
    py_files = find_py_files(PROJECT_ROOT)
    write_log(f"📁 Python files scanned: {len(py_files)}")

    suspicious_data = load_json(SUSPICIOUS_REPORT)
    usage_map = load_json(USAGE_MAP_PATH)

    if not suspicious_data:
        write_log("❌ Error: suspicious_code_report.json not found or empty.")
        return

    summary = {}

    for item in suspicious_data:
        file_path = os.path.join(PROJECT_ROOT, item.get("file", ""))
        issue_type = item.get("type", "")
        matches = item.get("matches", [])

        if not os.path.isfile(file_path):
            write_log(f"⚠️ Skipped (not found): {file_path}")
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except:
            write_log(f"❌ Error reading: {file_path}")
            continue

        insertions = []
        for match in matches:
            if not isinstance(match, str):
                continue
            for idx, line in enumerate(lines):
                if isinstance(line, str) and match in line:
                    marker = f"# @auto_flag: {issue_type} [{match}]"
                    suggestion = suggest_fix(issue_type, match)
                    insertions.append((idx, marker, suggestion))
                    break

        if insertions:
            new_lines = []
            inserted = set()
            for idx, line in enumerate(lines):
                if idx not in inserted:
                    relevant = [i for i in insertions if i[0] == idx]
                    for _, marker, suggestion in relevant:
                        new_lines.append(marker + '\n')
                        new_lines.append(suggestion + '\n')
                    if relevant:
                        inserted.add(idx)
                new_lines.append(line)

            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                write_log(f"✅ Updated: {file_path} ({len(insertions)} issues flagged)")
                summary[file_path] = len(insertions)
            except:
                write_log(f"❌ Failed to write: {file_path}")
        else:
            write_log(f"✅ Clean: {file_path}")

    write_log("----------------------------------------------------")
    write_log("📝 Correction Summary:")
    for path, count in summary.items():
        write_log(f" - {path}: {count} flags inserted")
    write_log("✅ Smart Correction Finished.")

if __name__ == "__main__":
    run_correction()
