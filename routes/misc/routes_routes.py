# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
# ────────────────────────────────────────────────────────────────
# 📁 FILE: routes/dev/routes_routes.py
# 📌 PURPOSE: Dev route tools for assist and duplication checks
# ────────────────────────────────────────────────────────────────
import os
from tools.obvious_router import auto_function
from handler import auto_route
from handler import auto_model
from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from handler import auto_logic

# @auto_function
router = APIRouter(prefix="/dev/routes", tags=["Dev Routes"])
templates = Jinja2Templates(directory="templates")

@auto_logic
@router.get("/routes", response_class=HTMLResponse)
# <smart.template>
async def show_routes_page(request: Request):
    return templates.TemplateResponse("dev/routes/routes.html", {"request": request})


@auto_model
@auto_route
def find_duplicate_routes():
    route_map = {}
    duplicates = []
    for root, _, files in os.walk("routes"):
        for file in files:
            if file.endswith("_routes.py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        if "route(" in line:
                            try:
                                route_path = line.split("'")[1]
                                if route_path in route_map:
                                    duplicates.append((route_path, route_map[route_path], path))
                                else:
                                    route_map[route_path] = path
                            except IndexError:
                                pass
    return duplicates


@router.post("/generate_assist")
async def trigger_generate_assist(data: dict):
    file_name = data.get("file_name")
    if not file_name:
        return JSONResponse(status_code=400, content={"error": "File name not provided."})
    # 🔧 Placeholder for actual logic
    # generate_assist(file_name)
    return {"message": f"Assistance triggered for {file_name}."}


@router.get("/duplicates")
async def show_duplicates():
    try:
        duplicates = find_duplicate_routes()
        if not duplicates:
            return {"message": "No duplicate routes found!"}
        return {"duplicates": duplicates}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.post("/search")
async def search_route(query: str = Form("/")):
    return RedirectResponse(url=query)
