# 📁 tools/ghost_template_router.py

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRoute
import os

def get_ghost_template_router(app, template_dir="templates"):
    router = APIRouter()
    templates = Jinja2Templates(directory=template_dir)

    # STEP 1: collect all existing route names (no override)
    registered_paths = set()
    for route in app.routes:
        if isinstance(route, APIRoute):
            registered_paths.add(route.path)

    # STEP 2: scan all .html templates
    for root, _, files in os.walk(template_dir):
        for file in files:
            if file.endswith(".html"):
                rel_path = os.path.relpath(os.path.join(root, file), template_dir)
                route_path = "/" + rel_path.replace(".html", "").replace("\\", "/").replace("/", "__")
                if route_path == "/index":
                    route_path = "/"

                if route_path in registered_paths:
                    continue  # already handled

                # STEP 3: dynamically bind fallback render
                def generate_handler(tpl):
                    async def handler(request: Request):
                        return templates.TemplateResponse(tpl, {"request": request})
                    return handler

                router.add_api_route(
                    route_path,
                    generate_handler(rel_path),
                    response_class=HTMLResponse,
                    name=f"{rel_path}_ghost"
                )

    return router
