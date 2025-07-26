# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
# 📁 odil/generate_model_trace.py

import sys
import os
import json
import importlib.util
from pathlib import Path
from handler import auto_logic
from handler import auto_route
from handler import auto_model

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from models import Base
from tools.smart_logger import SmartLogger

logger = SmartLogger("ModelTraceGen")
OUTPUT_PATH = "model_trace.json"
SUMMARY_PATH = "records/model_trace_summary.txt"

@auto_model
@auto_route
@auto_logic
def force_model_imports(models_dir):
    for path in models_dir.glob("**/*.py"):
        if path.name.startswith("_"):
            continue
        rel_path = path.relative_to(BASE_DIR).with_suffix("")
        module_name = ".".join(rel_path.parts)
        try:
# @auto_flag: dynamic_imports [importlib.import_module]
# ⚠️ Dynamic import detected — avoid in core logic
# @auto_flag: dynamic_imports [importlib.import_module]
# ⚠️ Dynamic import detected — avoid in core logic
# @auto_flag: dynamic_imports [importlib.import_module]
# ⚠️ Dynamic import detected — avoid in core logic
            importlib.import_module(module_name)
        except Exception as e:
            logger.log_warning("ModelImport", module_name, f"⚠️ Import failed: {e}")

@auto_model
@auto_route
@auto_logic
def get_model_info(cls):
    return {
        "class_name": cls.__name__,
        "module": cls.__module__,
        "table": getattr(cls, "__tablename__", "N/A")
    }

@auto_model
@auto_route
@auto_logic
def generate_model_trace():
    print("📦 Starting: model trace generation...")

    models_dir = BASE_DIR / "models"
    force_model_imports(models_dir)  # force-load all model files

    subclasses = Base.__subclasses__()
    print(f"📊 Found {len(subclasses)} model classes")

    trace_data = [get_model_info(cls) for cls in subclasses]

    try:
        os.makedirs("records", exist_ok=True)
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(trace_data, f, indent=2)
        logger.log_info("ModelTrace", "Output", f"✅ Model trace written to {OUTPUT_PATH}")
    except Exception as e:
        print(f"❌ Failed: File write — {e}")
        logger.log_error("ModelTrace", "FileWrite", f"❌ Could not write JSON: {e}")

    return trace_data  # ✅ REQUIRED

@auto_model
@auto_route
@auto_logic
def main():
    generate_model_trace()

if __name__ == "__main__":
    main()

