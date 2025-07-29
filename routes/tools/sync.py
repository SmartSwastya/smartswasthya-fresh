# ╭────────────────────────────────────────────────────────────╮
# │ 📂 ROUTE LAYER :: sync.py                                  │
# │ Description: Retry sync route — calls sync_retry_logic     │
# ╰────────────────────────────────────────────────────────────╯
# 📁 routes/dev/sync/sync.py

from fastapi import APIRouter, Request, Body
from fastapi.responses import JSONResponse

from tools.obvious_router import auto_route, auto_logic
from tools.smart_template import templates
from tools.dev.sync import sync_files_to_server

router = APIRouter(prefix="/dev/sync", tags=["Dev Sync"])


@auto_route
@auto_logic
@router.get("/sync")
async def show_sync_page(request: Request):
    return templates("sync.html", request=request)


@auto_route
@auto_logic
@router.post("/run")
async def run_sync(file_list: list[str] = Body(...)):
    result = sync_files_to_server(file_list)
    return JSONResponse(content=result)
