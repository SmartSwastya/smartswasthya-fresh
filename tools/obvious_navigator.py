# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# ==========================================================
# 🔍 Obvious Navigator
# Location: tools/obvious_navigator.py
# Purpose: Reads obvious_registry.json and explores contents
# ==========================================================

import os
import sys
import json
import ast
from pathlib import Path

from obvious_mapper import ObviousMapper

PROJECT_ROOT = str(Path(__file__).resolve().parents[2])
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

BASE_DIR = str(Path(__file__).resolve().parents[1])
REGISTRY_PATH = str(Path(__file__).resolve().parent.parent / "obvious_registry.json")

@auto_model
@auto_route
@auto_logic
def load_registry():
    if not os.path.exists(REGISTRY_PATH):
        raise FileNotFoundError("obvious_registry.json not found.")
    with open(REGISTRY_PATH, "r") as file:
        return json.load(file)

@auto_model
@auto_route
@auto_logic
def list_python_files(directory):
    return [
        f for f in os.listdir(directory)
        if f.endswith(".py") and not f.startswith("__")
    ]

@auto_model
@auto_route
@auto_logic
def extract_functions_and_classes(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    items = {
        "functions": [],
        "classes": []
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            items["functions"].append(node.name)
        elif isinstance(node, ast.ClassDef):
            items["classes"].append(node.name)

    return items

@auto_model
@auto_route
@auto_logic
def explore_all():
    registry = load_registry()
    structure = {}

    for module_name, meta in registry.items():
        if "abs_path" not in meta:
            print(f"⚠️ Warning: 'abs_path' missing in: {meta}")
        abs_path = meta.get("abs_path", "❌ abs_path missing")
        structure[module_name] = {}

        try:
            files = list_python_files(abs_path)
            for fname in files:
                full_path = os.path.join(abs_path, fname)
                structure[module_name][fname] = extract_functions_and_classes(full_path)
        except Exception as e:
            structure[module_name]["__error__"] = str(e)

    return structure

class ObviousNavigator:
    @classmethod
    @auto_model
    @auto_route
    @auto_logic
    def navigate(cls):
        print("Navigating via ObviousNavigator")
        # 🚧 Add actual navigation logic here later

if __name__ == "__main__":
    from pprint import pprint
    pprint(explore_all())

