# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic, auto_route, auto_model
from tools.smart_logger import SmartLogger

import os
import sys
import ast
import json
from pathlib import Path

# ==== 🧠 Logger Setup ====
logger = SmartLogger("LogicTraceGen")
TRACE_DEBUG = False

# ==== 📁 Path Setup ====
PROJECT_ROOT = str(Path(__file__).resolve().parents[1])
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

LOGIC_DIR = os.path.join(PROJECT_ROOT, "logic")
OUTPUT_FILE = "logic_trace.json"
SUMMARY_FILE = "records/logic_trace_summary.txt"


# ==== 🛠️ Utility Logger ====
def debug_log(msg, summary_lines):
    if TRACE_DEBUG:
        print(msg)
    summary_lines.append(msg)


# ==== 🔍 Function Scanner ====
@auto_model
@auto_route
@auto_logic
def extract_logic_functions():
    logic_functions = []
    summary_lines = []

    if not os.path.isdir(LOGIC_DIR):
        msg = f"⚠️ Skipped: Directory not found → {LOGIC_DIR}"
        print(msg)
        logger.log_warning("LogicTrace", "Init", msg)
        debug_log(msg, summary_lines)
        return logic_functions, summary_lines

    for root, _, files in os.walk(LOGIC_DIR):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        source = f.read()
                    tree = ast.parse(source, filename=file_path)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            if node.name.startswith(("run", "apply", "custom_")):
                                logic_functions.append({
                                    "function": node.name,
                                    "file": file_path.replace("\\", "/")
                                })
                                msg = f"✅ {file} → {node.name}"
                                logger.log_success("LogicFn", file, f"Found: {node.name}")
                                debug_log(msg, summary_lines)
                except Exception as e:
                    err = f"⚠️ Error in {file_path}: {e}"
                    print(err)
                    logger.log_warning("LogicTrace", file_path, err)
                    debug_log(err, summary_lines)

    return logic_functions, summary_lines


# ==== 🧾 Main Trace Generator ====
@auto_model
@auto_route
@auto_logic
def generate_logic_trace():
    print("📦 Starting: logic trace generation...")
    logger.log_info("LogicTrace", "Start", "🧠 Scanning logic/ directory...")

    logic_data, summary = extract_logic_functions()

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(logic_data, f, indent=2)
        print(f"✅ Done: {OUTPUT_FILE} with {len(logic_data)} functions")
        logger.log_info("LogicTrace", "Output", f"📝 Written to {OUTPUT_FILE}")
    except Exception as e:
        err = f"❌ Failed: could not write {OUTPUT_FILE} — {e}"
        print(err)
        logger.log_error("LogicTrace", "FileWrite", err)

    try:
        os.makedirs("records", exist_ok=True)
        with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(summary))
    except Exception as e:
        print(f"❌ Could not save logic summary: {e}")

    return logic_data


# ==== 🟢 Entry Point ====
@auto_model
@auto_route
@auto_logic
def main():
    generate_logic_trace()


if __name__ == "__main__":
    generate_logic_trace()
