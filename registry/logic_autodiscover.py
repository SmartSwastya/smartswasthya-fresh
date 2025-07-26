# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
import importlib
import pkgutil
import inspect
from tools.smart_logger import SmartLogger

logger = SmartLogger("LogicAutoDiscover")

@auto_model
@auto_route
@auto_logic
def auto_register_logic():
    base_package = "logic"
    registered = []
    for finder, name, ispkg in pkgutil.walk_packages([base_package], prefix=f"{base_package}."):
        try:
# @auto_flag: dynamic_imports [importlib.import_module]
# ⚠️ Dynamic import detected — avoid in core logic
# @auto_flag: dynamic_imports [importlib.import_module]
# ⚠️ Dynamic import detected — avoid in core logic
# @auto_flag: dynamic_imports [importlib.import_module]
# ⚠️ Dynamic import detected — avoid in core logic
            module = importlib.import_module(name)
            functions = dir(module)
            if "run" in functions or "apply" in functions:
                registered.append(name)
                logger.log_success("Logic", name, f"✅ Imported {name}")
            else:
                logger.log_warning("Logic", name, "Missing function: 'run' or 'apply'")
        except Exception as e:
            logger.log_failure("Logic", name, f"Import error: {str(e)}")

    logger.log_note("Logic", f"{len(registered)} logic modules registered")
    print(logger.summarize("Logic"))

@auto_model
@auto_route
@auto_logic
def get_logic_function(module_name: str, func_name: str = "run"):
    try:
        module = importlib.import_module(module_name)
        if hasattr(module, func_name):
            return getattr(module, func_name)
        # Fallback logic
        elif func_name == "run" and hasattr(module, "apply"):
            return getattr(module, "apply")
        elif func_name == "apply" and hasattr(module, "run"):
            return getattr(module, "run")
        else:
            return None
    except Exception:
        return None
