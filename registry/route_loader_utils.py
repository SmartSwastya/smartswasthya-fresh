# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
# registry/route_loader_utils.py

import os
import importlib.util
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

def get_all_route_files():
    route_files = []
    target_dirs = ["routes", "blueprints"]

    for folder in target_dirs:
        folder_path = os.path.join(ROOT_DIR, folder)
        if not os.path.isdir(folder_path):
            continue

        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    route_files.append(os.path.join(root, file))

    return route_files

def import_module_from_path(file_path):
    try:
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            return None
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        return None

