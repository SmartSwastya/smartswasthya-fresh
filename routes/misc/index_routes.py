# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_route
from tools.smart_marker_injector import auto_function
# @auto_route
from tools.obvious_router import auto_function
# @auto_function
# routes/index_routes.py

from fastapi import APIRouter
from handler import auto_logic, auto_model
from tools.obvious_router import auto_route

router = APIRouter()

@router.get("/api/index", operation_id="get_api_index")
@auto_model
@auto_route
@auto_logic
def hello():
    return {"message": "Hello from index_routes"}
