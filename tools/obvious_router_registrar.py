# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# tools/obvious_router_registrar.py

import os
import sys
import importlib.util
from fastapi.routing import APIRouter
from registry.route_loader_utils import get_all_route_files, import_module_from_path
from tools.smart_logger import SmartLogger

logger = SmartLogger("RouterRegistrar")

@auto_model
@auto_route
@auto_logic
def register_all_routes():
    logger.log_info("Router", "Registry", "🔎 Scanning for route files...")
    route_files = get_all_route_files()
    registered_routes = []

    for path in route_files:
        module = import_module_from_path(path)
        if not module:
            logger.log_warning("Router", path, "⚠️ Could not import module")
            continue

        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, APIRouter):
                registered_routes.append({
                    "router": attr,
                    "source": path,
                    "var_name": attr_name,
                })
                logger.log_success("Router", path, f"✅ Found router: {attr_name}")
                break  # One router per file is enough

    logger.log_info("Router", "Registry", f"📦 Total routers discovered: {len(registered_routes)}")
    return registered_routes

