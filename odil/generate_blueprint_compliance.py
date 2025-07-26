# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic, auto_route, auto_model
from tools.smart_logger import SmartLogger
from odil.utils import load_json_data
from registry.route_loader_utils import get_all_route_files
from tools.obvious_router_registrar import register_all_routes

import os
import sys
import json
from pathlib import Path

# ==== 🧠 Logger Setup ====
logger = SmartLogger("BlueprintCompliance")
TRACE_DEBUG = False  # Toggle detailed logs

# ==== 📁 Path Setup ====
PROJECT_ROOT = str(Path(__file__).resolve().parents[1])
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ==== 🧾 Debug helper ====
def debug(msg, summary_lines):
    if TRACE_DEBUG:
        print(msg)
    summary_lines.append(msg)


# ==== 🔍 Main Compliance Checker ====
@auto_model
@auto_route
@auto_logic
def trace_blueprint_compliance():
    print("📦 Starting: blueprint compliance generation...")
    logger.log_info("Blueprint", "Start", "📦 Starting compliance check...")

    summary_lines = []
    debug("🔍 Running V4 Blueprint Compliance Check...\n", summary_lines)

    trace_files = {
        "function_trace": "function_trace.json",
        "function_usage_map": "function_usage_map.json",
        "logic_trace": "logic_trace.json",
        "model_trace": "model_trace.json",
        "route_trace": "route_trace.json",
    }

    blueprints = {}
    for key, path in trace_files.items():
        try:
            full_path = path if os.path.exists(path) else os.path.join("..", path)
            blueprints[key] = load_json_data(full_path)
            debug(f"✅ Loaded {key} ({len(blueprints[key])} entries)", summary_lines)
        except Exception as e:
            debug(f"❌ Error loading {key} from {path}: {e}", summary_lines)
            blueprints[key] = []

    compliance_report = {
        "missing_functions": [],
        "unused_functions": [],
        "unlinked_models": [],
        "missing_models": [],
        "orphan_logic_modules": [],
        "missing_routes": [],
        "ghost_routers": [],
        "unmatched_dev_sources": [],
        "unmatched_router_sources": [],
    }

    route_files = get_all_route_files()
    registered_routes = register_all_routes()

    expected_routes = set()
    actual_routes = set(r["source"] for r in registered_routes if "source" in r)

    for entry in blueprints.get("route_trace", []):
        if isinstance(entry, dict):
            expected_routes.add(entry.get("route_file") or entry.get("file") or entry.get("source"))
        elif isinstance(entry, str):
            expected_routes.add(entry)

    compliance_report["missing_routes"] = sorted(expected_routes - actual_routes)
    compliance_report["ghost_routers"] = sorted(actual_routes - expected_routes)

    actual_model_names = {
        m["model_name"]
        for m in blueprints.get("model_trace", [])
        if isinstance(m, dict) and "model_name" in m
    }
    declared_model_names = set()
    for usage in blueprints.get("function_usage_map", []):
        if isinstance(usage, dict) and "models_used" in usage:
            declared_model_names.update(usage["models_used"])

    compliance_report["missing_models"] = sorted(declared_model_names - actual_model_names)
    compliance_report["unlinked_models"] = sorted(actual_model_names - declared_model_names)

    defined_functions = {
        f.get("function_name") or f.get("name")
        for f in blueprints.get("function_trace", [])
        if isinstance(f, dict)
    }
    used_functions = {
        u["function_name"]
        for u in blueprints.get("function_usage_map", [])
        if isinstance(u, dict) and "function_name" in u
    }

    compliance_report["missing_functions"] = sorted(used_functions - defined_functions)
    compliance_report["unused_functions"] = sorted(defined_functions - used_functions)

    declared_logic_modules = {
        l["module_name"]
        for l in blueprints.get("logic_trace", [])
        if isinstance(l, dict) and "module_name" in l
    }
    used_logic_modules = set()
    for usage in blueprints.get("function_usage_map", []):
        if isinstance(usage, dict) and "logic_modules" in usage:
            used_logic_modules.update(usage["logic_modules"])

    compliance_report["orphan_logic_modules"] = sorted(declared_logic_modules - used_logic_modules)

    # Optional: Dev vs Router trace source diff
    if blueprints.get("dev_trace") and blueprints.get("router_map"):
        dev_files = {
            d["file"]
            for d in blueprints["dev_trace"]
            if isinstance(d, dict) and "file" in d
        }
        router_files = {
            r["source"]
            for r in blueprints["router_map"]
            if isinstance(r, dict) and "source" in r
        }
        compliance_report["unmatched_dev_sources"] = sorted(dev_files - router_files)
        compliance_report["unmatched_router_sources"] = sorted(router_files - dev_files)

    # ==== 💾 Save Outputs ====
    try:
        os.makedirs("odil", exist_ok=True)
        with open("odil/blueprint_compliance_report.json", "w", encoding="utf-8") as f:
            json.dump(compliance_report, f, indent=2)
        print("✅ Done: blueprint_compliance_report.json saved")
        logger.log_success("Blueprint", "Report", "📝 Compliance report saved")
    except Exception as e:
        print(f"❌ Failed: writing report — {e}")
        logger.log_error("Blueprint", "Write", f"❌ Report write error: {e}")

    try:
        os.makedirs("records", exist_ok=True)
        with open("records/blueprint_compliance_summary.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(summary_lines))
    except Exception as e:
        print(f"❌ Failed: writing summary — {e}")


# ==== 🟢 Entry Point ====
if __name__ == "__main__":
    trace_blueprint_compliance()
