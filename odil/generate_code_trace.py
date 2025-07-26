# generate_code_trace.py
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
import os, sys, ast, json
from collections import defaultdict
from tools.smart_logger import SmartLogger
from handler import auto_model, auto_route, auto_logic

logger = SmartLogger("CodeTraceGen")
OUTPUT_FILE = "function_trace.json"
SUMMARY_FILE = "records/code_trace_summary.txt"
TRACE_DEBUG = False

# ==== Auto Project Root ====
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(FILE_DIR, ".."))
sys.path.insert(0, PROJECT_ROOT)

def debug_log(msg, summary_lines):
    if TRACE_DEBUG:
        print(msg)
    summary_lines.append(msg)

@auto_model
@auto_route
@auto_logic
def extract_defined_functions():
    functions = []
    summary_lines = []
    traced_dirs = set()

    for root, _, files in os.walk(PROJECT_ROOT):
        if any(x in root for x in ["/.git", "/venv", "/node_modules", "/__pycache__"]):
            continue
        for file in files:
            if not file.endswith(".py") or file.startswith("__"):
                continue

            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, PROJECT_ROOT).replace("\\", "/")
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    source = f.read()
                tree = ast.parse(source, filename=file_path)

                found = False
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        functions.append({
                            "function": node.name,
                            "file": rel_path,
                            "lineno": node.lineno
                        })
                        logger.log_success("Function", rel_path, f"{node.name} (Line {node.lineno})")
                        debug_log(f"✅ {rel_path} :: def {node.name} (line {node.lineno})", summary_lines)
                        found = True

                # ✅ Force-register file-level trace marker
                if not found and "__trace_marker__" in source:
                    functions.append({
                        "function": "__trace_marker__",
                        "file": rel_path,
                        "lineno": 1
                    })
                    logger.log_info("Marker", rel_path, "📍 Marker detected (__trace_marker__)")
                    debug_log(f"📍 {rel_path} :: __trace_marker__ (forced)", summary_lines)

                # ✅ Directory-level trace marker fallback
                if "__trace_marker__" in source:
                    dir_name = rel_path.split("/")[0]
                    if dir_name not in traced_dirs:
                        traced_dirs.add(dir_name)
                        functions.append({
                            "function": "__trace_marker__",
                            "file": dir_name,
                            "lineno": 0
                        })
                        logger.log_info("DirMarker", dir_name, "📦 Module traced via marker")
                        debug_log(f"📦 {dir_name}/ :: __trace_marker__ (directory marker)", summary_lines)

            except Exception as e:
                logger.log_warning("CodeTrace", rel_path, f"⚠️ Skipped due to error: {e}")
                debug_log(f"⚠️ {rel_path} :: {e}", summary_lines)

    grouped = defaultdict(list)
    for fn in functions:
        key = fn["file"].split("/")[0].replace(".py", "")
        grouped[key].append(fn)

    dual_output = {"_flat": functions, **dict(sorted(grouped.items()))}
    return dual_output, summary_lines

@auto_model
@auto_route
@auto_logic
def generate_code_trace():
    print("📦 Starting: code trace generation...")
    logger.log_info("CodeTrace", "Start", "🔍 Scanning for function definitions...")

    grouped_data, summary = extract_defined_functions()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(grouped_data, f, indent=2)
    print(f"✅ Done: {OUTPUT_FILE} with {len(grouped_data['_flat'])} functions across {len(grouped_data) - 1} modules")

    os.makedirs("records", exist_ok=True)
    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(summary))

if __name__ == "__main__":
    generate_code_trace()
