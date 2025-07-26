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
import re
import logging

@auto_model
@auto_route
@auto_logic
def handle_route_duplicates():
    """
    Detects and reports include_router duplications across route files.
    """
    root_dir = "routes"
    route_includes = {}
    duplicate_found = False

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception as e:
                    logging.warning(f"❌ Cannot read {file_path}: {e}")
                    continue

                includes = re.findall(r'include_router\((.*?)\)', content)
                for inc in includes:
                    if inc not in route_includes:
                        route_includes[inc] = []
                    route_includes[inc].append(file_path)

    for inc, files in route_includes.items():
        if len(files) > 1:
            logging.warning(f"\n🚨 Duplicate include_router for '{inc}' found in:")
            for f in files:
                logging.warning(f"   └─ {f}")
            duplicate_found = True

    if not duplicate_found:
        logging.info("✅ No duplicate route includes found.")

