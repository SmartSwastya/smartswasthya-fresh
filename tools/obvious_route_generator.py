# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# ============================================================
# 📁 FILE: tools/obvious_route_generator.py
# 📌 PURPOSE: Scans a folder and dynamically generates FastAPI route bindings
# ============================================================

import importlib.util
import os
from fastapi import APIRouter

@auto_model
@auto_route
@auto_logic
def generate_routes_for_directory(directory_path, app=None):
    for filename in os.listdir(directory_path):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            module_path = os.path.join(directory_path, filename)

            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for attr in dir(module):
                obj = getattr(module, attr)
                if isinstance(obj, APIRouter) and app:
                    app.include_router(obj)
                    print(f"✅ Registered router from {filename} via {attr}")
                    break

