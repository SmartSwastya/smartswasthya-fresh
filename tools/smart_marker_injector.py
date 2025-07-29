# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
import os
import json
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path

# === CONFIG ===
ROOT_DIR = Path(__file__).resolve().parent.parent

TRACE_PATHS = {
    "model": ROOT_DIR / "model_trace.json",
    "function": ROOT_DIR / "function_trace.json",
    "route": ROOT_DIR / "route_trace.json",
    "template": ROOT_DIR / "template_trace.json",
    "logic": ROOT_DIR / "logic_trace.json",
    "circuit": ROOT_DIR / "tools" / "circuit_trace.json",
}

MARKER_MAP = {
    "model":    ("# @auto_model",    "from tools.smart_marker_injector import auto_model"),
    "route":    ("# @auto_route",    "from tools.smart_marker_injector import auto_route"),
    "logic":    ("# @auto_logic",    "from tools.smart_marker_injector import auto_logic"),
    "task":     ("# @auto_task",     "from tools.smart_marker_injector import auto_task"),
    "template": ("# @auto_template", "from tools.smart_marker_injector import auto_template"),
    "function": ("# @auto_function", "from tools.smart_marker_injector import auto_function"),
}

EXCLUDE_DIRS = {"__pycache__", ".git", ".idea", ".vscode", "site-packages"}
LOG_DIR = ROOT_DIR / "records" / "marker_logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

summary = {
    "injected": [], "already_ok": [], "removed": [],
    "corrupt_fixed": [], "missing_file": [], "unknown_type": []
}

# === HELPERS ===
def load_trace(trace_type: str) -> List[Dict[str, Any]]:
    trace_file = TRACE_PATHS[trace_type]
    if not trace_file.exists():
        return []
    with open(trace_file, "r", encoding="utf-8") as f:
        raw = json.load(f)

    traces = []
    if trace_type == "function":
        for filename, functions in raw.items():
            for fdef in functions:
                fdef["file"] = filename
                fdef["type"] = "function"
                traces.append(fdef)
    elif trace_type == "logic":
        for entry in raw:
            entry["type"] = "logic"
            traces.append(entry)
    else:
        for entry in raw:
            entry["type"] = trace_type
            traces.append(entry)

    return traces

def load_json(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def build_marker_map():
    file_marker_map = {}
    self_path = str(Path(__file__).resolve())

    for trace_type, path in TRACE_PATHS.items():
        if not path.exists():
            continue
        for record in load_json(path):
            file = record.get("file") or record.get("source_file")
            if not file:
                continue
            file_path = str(Path(file).resolve())

            # ✅ Self-exclude this script itself
            if file_path == self_path:
                continue

            if "tools/obvious_router.py" in file_path.replace("\\", "/"):
                continue
            file_marker_map.setdefault(file_path, set()).add(trace_type)
    return file_marker_map

def apply_patch(file_path, expected_types):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except:
        summary["missing_file"].append(file_path)
        return

    original = lines[:]
    present_markers = set()
    present_imports = set()

    for line in lines:
        for mtype, (marker, imp) in MARKER_MAP.items():
            if marker in line:
                present_markers.add(mtype)
            if imp in line:
                present_imports.add(mtype)

    insert_pos = 0
    expected_types_cleaned = [t.strip().lower() for t in expected_types]

    for mtype in expected_types_cleaned:
        if mtype not in MARKER_MAP:
            summary["unknown_type"].append((file_path, mtype))
            continue

        marker, imp = MARKER_MAP[mtype]
        if mtype not in present_imports:
            lines.insert(insert_pos, imp + "\n"); insert_pos += 1
        if mtype not in present_markers:
            lines.insert(insert_pos, marker + "\n"); insert_pos += 1
            summary["injected"].append((file_path, marker))
        else:
            summary["already_ok"].append((file_path, marker))

    for mtype, (marker, imp) in MARKER_MAP.items():
        if mtype not in expected_types_cleaned:
            lines = [l for l in lines if marker not in l and imp not in l]
            summary["removed"].append((file_path, marker))

    seen = set()
    cleaned_lines = []
    for line in lines:
        line_strip = line.strip()
        if any(marker in line_strip for marker, _ in MARKER_MAP.values()):
            if line_strip in seen:
                summary["corrupt_fixed"].append((file_path, line_strip))
                continue
            seen.add(line_strip)
        cleaned_lines.append(line)

    if cleaned_lines != original:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(cleaned_lines)

def recursive_injector():
    print("📁 LIVE PATH:", __file__)

    for file_path, expected_types in build_marker_map().items():
        apply_patch(file_path, expected_types)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOG_DIR / f"{timestamp}_marker_report.log"
    with open(log_file, "w", encoding="utf-8") as f:
        for key, entries in summary.items():
            f.write(f"\n=== {key.upper()} ===\n")
            for entry in entries:
                f.write(str(entry) + "\n")

    print(f"\n✅ Marker Injection Complete.\n📄 Log: {log_file.name}")

# EXPORT HOOKS
__all__ = ["auto_model", "auto_route", "auto_logic", "auto_task", "auto_template"]
def auto_model(cls): return cls
def auto_route(func): return func
def auto_logic(func): return func
def auto_task(func): return func
def auto_template(func): return func
def auto_function(x): return x

if __name__ == "__main__":
    recursive_injector()
