# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
import logging
from fastapi.routing import APIRoute

@auto_model
@auto_route
@auto_logic
def detect_route_conflicts(app):
    """
    Scans FastAPI app for duplicate path+method conflicts.
    """
    route_map = {}
    conflicts = []

    for route in app.routes:
        if isinstance(route, APIRoute):
            path = route.path
            for method in route.methods:
                key = (path, method)
                if key in route_map:
                    conflicts.append({
                        "path": path,
                        "method": method,
                        "conflict_with": route_map[key].name,
                        "current": route.name
                    })
                else:
                    route_map[key] = route

    if conflicts:
        logging.warning("🚨 Route conflicts detected:")
        for conflict in conflicts:
            logging.warning(f"🔁 {conflict['method']} {conflict['path']} — "
                            f"Conflicts: {conflict['current']} vs {conflict['conflict_with']}")
    else:
        logging.info("✅ No route conflicts found.")

