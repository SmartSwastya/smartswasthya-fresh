# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# odil/generate_obvious_connections.py

# ----------------------------------------------
# 🔗 Obvious Connections Generator
# ----------------------------------------------
# Merges all trace files (route, template, logic, models, usage map)
# into one smart map called obvious_connections.json
# ----------------------------------------------

import json
import sys, os
from pathlib import Path
from tools.smart_logger import SmartLogger

logger = SmartLogger("ObviousConnGen")

# -------------------------------
# ✳️ PATH DEFINITIONS
# -------------------------------
PROJECT_ROOT = str(Path(__file__).resolve().parents[1])
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

ODIL_DIR = os.path.dirname(__file__)
OUTPUT_FILE = os.path.join(ODIL_DIR, "obvious_connections.json")

@auto_model
@auto_route
@auto_logic
def read_json(name):
    path_map = {
        "template_trace.json": os.path.join(ODIL_DIR, "template_trace.json")
    }
    path = path_map.get(name, os.path.join(PROJECT_ROOT, name))
    if not os.path.exists(path):
        logger.log_error("Missing", name, "File not found")
        raise FileNotFoundError(f"❌ {name} not found")
    with open(path, encoding="utf-8") as f:
        return json.load(f)

@auto_model
@auto_route
@auto_logic
def generate_obvious_connections():
    print("📦 Starting: obvious connections map generation...")  # ✅ STDOUT START
    logger.log_info("ObviousConn", "Start", "📦 Aggregating trace files...")

    route_trace = read_json("route_trace.json")
    template_trace = read_json("template_trace.json")
    model_trace = read_json("model_trace.json")
    logic_trace = read_json("logic_trace.json")
    function_usage_map = read_json("function_usage_map.json")

    if not all([route_trace, template_trace, model_trace, logic_trace, function_usage_map]):
        print("❌ Failed: One or more trace files could not be loaded.")
        return

    obvious_map = {}

    for route_module in route_trace:
        module = route_module.get("path")
        entry = {
            "templates": [],
            "used_functions": [],
            "logic_files": [],
            "models": [],
            "status": "active"
        }

        for tpl in template_trace:
            if isinstance(tpl, dict) and tpl.get("used_in_module") == module:
                entry["templates"].append(tpl.get("template"))

        for func, files in function_usage_map.items():
            for f in files:
                if f == f"{module}.py" or f == module:
                    entry["used_functions"].append(func)

        for logic_item in logic_trace:
            if isinstance(logic_item, dict) and logic_item.get("used_in_module") == module:
                entry["logic_files"].append(logic_item.get("file"))

        for model in model_trace:
            if isinstance(model, dict) and model.get("used_in_module") == module:
                entry["models"].append(model.get("file"))
            elif isinstance(model, str) and model == module:
                entry["models"].append(model)

        if not entry["templates"]:
            entry["status"] = "placeholder"

        obvious_map[module] = entry

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(obvious_map, f, indent=2)
        print(f"✅ Done: obvious_connections.json with {len(obvious_map)} entries")  # ✅ STDOUT SUCCESS
        logger.log_success("ObviousConn", "Output", f"📝 Written to {OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ Failed: writing {OUTPUT_FILE} — {e}")
        logger.log_error("ObviousConn", "FileWrite", f"❌ Failed to write output: {e}")

if __name__ == "__main__":
    generate_obvious_connections()

