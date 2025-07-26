# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
import os
import importlib.util
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ROUTES_DIRS = ["routes", "blueprints"]

@auto_model
@auto_route
@auto_logic
def get_all_router_objects():
    router_list = []

    for subdir in ROUTES_DIRS:
        dir_path = PROJECT_ROOT / subdir
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, PROJECT_ROOT)
                    module_name = rel_path.replace(os.sep, ".").replace(".py", "")

                    try:
                        spec = importlib.util.spec_from_file_location(module_name, full_path)
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        router = getattr(module, "router", None)
                        if router:
                            router_list.append({
                                "label": module_name,
                                "source": rel_path,
                                "router": router
                            })
                    except Exception as e:
                        print(f"⚠️ Error importing {module_name}: {e}")

    return router_list
