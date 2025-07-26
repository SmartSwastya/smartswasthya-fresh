# ╔══════════════════════════════════════════════════════════════════╗
# ║ ✅ model_registry.py — SQLAlchemy Model Collector               ║
# ║ 📦 Discovers valid model classes from models/ directory         ║
# ║ 🔍 Uses DeclarativeMeta to filter real SQLAlchemy models        ║
# ╚══════════════════════════════════════════════════════════════════╝

import os
import sys
import importlib.util
from sqlalchemy.orm import DeclarativeMeta
from tools.smart_logger import SmartLogger

from handler import auto_logic, auto_route, auto_model
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function

logger = SmartLogger("ModelRegistry")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
MODELS_DIR = os.path.join(ROOT_DIR, "models")

@auto_model
@auto_route
@auto_logic
def get_all_model_classes():
    """
    Recursively import all .py files in models/ and extract valid
    SQLAlchemy DeclarativeMeta classes, avoiding re-import warnings.
    """
    model_classes = []
    seen_modules = set()

    if not os.path.isdir(MODELS_DIR):
        logger.log_warning("Model", "DirectoryCheck", "⚠️ 'models/' directory not found")
        return model_classes

    for root, _, files in os.walk(MODELS_DIR):
        for file in files:
            if not file.endswith(".py") or file.startswith("__"):
                continue

            file_path = os.path.join(root, file)
            rel_module_path = os.path.relpath(file_path, ROOT_DIR).replace(os.sep, ".")
            module_name = rel_module_path.rsplit(".py", 1)[0]

            if module_name in seen_modules or module_name in sys.modules:
                logger.log_warning("Model", module_name, "⚠️ Duplicate or already-loaded module skipped.")
                continue

            try:
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                seen_modules.add(module_name)

                found = 0
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and isinstance(attr, DeclarativeMeta):
                        model_classes.append(attr)
                        found += 1
                        logger.log_success("Model", module_name, f"✅ Found model: {attr_name}")

                if not found:
                    logger.log_note("Model", module_name, "ℹ️ No valid DeclarativeMeta models in this file")

            except Exception as e:
                logger.log_warning("Model", module_name, f"⚠️ Skipped due to import error: {e}")

    logger.log_info("Model", "Summary", f"📦 Total models discovered: {len(model_classes)}")
    return model_classes
