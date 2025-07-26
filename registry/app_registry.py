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
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRoute
from fastapi import APIRouter

from tools.obvious_router_registrar import register_all_routes
from obvious_mapper import ObviousMapper

# ========================================================
# 📁 SECTION: App Registry Setup
# 🔹 Location: D:\root\smartswasthya\registry\app_registry.py
# 🔸 Purpose: Central app binding via ObviousMapper + Auto Router Injector
# ========================================================

# ========================================================
# 🧠 SECTION: Manual + Auto FastAPI App Integration
# ========================================================
@auto_model
@auto_route
@auto_logic
def setup_app(app: FastAPI):
    print("⚙️ Starting Obvious App Setup...")

    # 🔁 Run mapper first (routing+function link)
    ObviousMapper.run()

    # ✅ Register all routes discovered recursively
    for router_info in register_all_routes():
        app.include_router(router_info["router"])

    # ✅ Auto-Include All Valid Routers from routes/
    base_dir = os.path.dirname(os.path.dirname(__file__))
    routes_dir = os.path.join(base_dir, "routes")

    for root, dirs, files in os.walk(routes_dir):
        for file in files:
            if file.endswith("_routes.py"):
                module_path = os.path.join(root, file)
                rel_path = os.path.relpath(module_path, base_dir)
                module_name = rel_path.replace(os.sep, ".").rsplit(".py", 1)[0]

                try:
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    if hasattr(module, "router"):
                        app.include_router(module.router)
                        print(f"✅ Auto-Registered Router: {module_name}")
                except Exception as e:
                    print(f"❌ Failed to load {module_name}: {e}")

    # ✅ Inject fallback renderer for ghost templates (auto .html render if not registered)
    templates_dir = os.path.join(base_dir, "templates")
    ghost_router = APIRouter()
    templates = Jinja2Templates(directory=templates_dir)

    registered_paths = set()
    for route in app.routes:
        if isinstance(route, APIRoute):
            registered_paths.add(route.path)

    for root, _, files in os.walk(templates_dir):
        for file in files:
            if file.endswith(".html"):
                rel_path = os.path.relpath(os.path.join(root, file), templates_dir)
                route_path = "/" + rel_path.replace(".html", "").replace("\\", "/").replace("/", "__")
                if route_path == "/index":
                    route_path = "/"
                if route_path in registered_paths:
                    continue

                def make_handler(tpl):
                    async def handler(request: Request):
                        return templates.TemplateResponse(tpl, {"request": request})
                    return handler

                ghost_router.add_api_route(
                    route_path,
                    make_handler(rel_path),
                    response_class=HTMLResponse,
                    name=f"{rel_path}_ghost"
                )

    app.include_router(ghost_router)

    print("✅ App setup complete.\n")
    return "App setup complete"
