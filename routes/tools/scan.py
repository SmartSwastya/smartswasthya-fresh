# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# ╔════════════════════════════════════════════════════════════════════╗
# ║            SMART SWASTHYA V3 – FILE SCAN ROUTES (FastAPI)         ║
# ║    Uses file_scanner.py for reusable logic across dev tools       ║
# ╚════════════════════════════════════════════════════════════════════╝

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from datetime import datetime
from utils.file_scanner import filter_files_by_time, list_all_files
import os
from tools.smart_marker_injector import auto_route
from tools.obvious_router import auto_route

router = APIRouter()

# Set root dir to scan
BASE_DIR = os.path.abspath(".")

# ════════════════════════════════════════
# 🔎 GET: List All .py Files
# ════════════════════════════════════════
# @auto_route
@router.get("/scan/all", operation_id="get_scan_all")
@auto_model
@auto_route
@auto_logic
def list_all_python_files():
    files = list_all_files(BASE_DIR, extension=".py")
    return JSONResponse(content={"files": files, "count": len(files)})

# ════════════════════════════════════════
# 🔍 POST: Scan Files by Modified Time
# ════════════════════════════════════════
@router.post("/scan/modified", operation_id="post_scan_modified")
@auto_model
@auto_route
@auto_logic
def scan_by_time(start_time: str = Query(...), end_time: str = Query(...)):
    """
    Example format: 2025-05-29T10:00:00
    """
    try:
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
    except ValueError:
        return JSONResponse(status_code=400, content={"error": "Invalid datetime format. Use ISO format."})

    modified_files = filter_files_by_time(BASE_DIR, start, end)
    return JSONResponse(content={"files": modified_files, "count": len(modified_files)})

