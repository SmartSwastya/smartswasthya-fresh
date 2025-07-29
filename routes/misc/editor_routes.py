# 📁 routes/dev/editor_routes.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
import os
from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from tools.obvious_router import auto_route
from handler import auto_logic, auto_model
from tools.smart_template import templates

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Router Setup                          ║
# ╚════════════════════════════════════════════════╝
router = APIRouter(prefix="/dev/editor", tags=["Dev Editor"])
BASE_DIR = Path(".")
history = {}  # Global edit history tracker


# ╔════════════════════════════════════════════════╗
# ║ SECTION: Editor UI Route                       ║
# ╚════════════════════════════════════════════════╝
@auto_model
@auto_route
@auto_logic
@router.get("")
def show_editor_page(request: Request):
    return templates.TemplateResponse("editor.html", {"request": request})


# ╔════════════════════════════════════════════════╗
# ║ SECTION: API – Load File                       ║
# ╚════════════════════════════════════════════════╝
@auto_model
@auto_route
@auto_logic
@router.get("/api/file")
def load_file(name: str):
    path = BASE_DIR / name
    if not path.exists():
        return JSONResponse(content={"success": False, "message": "File not found"})
    try:
        content = path.read_text(encoding="utf-8")
        return {"success": True, "content": content}
    except Exception as e:
        return {"success": False, "message": str(e)}


# ╔════════════════════════════════════════════════╗
# ║ SECTION: API – Get File by Path                ║
# ╚════════════════════════════════════════════════╝
@auto_model
@auto_route
@auto_logic
@router.get("/api/editor/file/{filename:path}")
def get_file(filename: str):
    try:
        content = Path(filename).read_text(encoding="utf-8")
        return {"content": content}
    except Exception as e:
        return JSONResponse(status_code=404, content={"error": str(e)})


# ╔════════════════════════════════════════════════╗
# ║ SECTION: API – List Files                      ║
# ╚════════════════════════════════════════════════╝
@auto_model
@auto_route
@auto_logic
@router.get("/api/editor/files")
def list_files():
    files = []
    for root, _, filenames in os.walk("routes"):
        for fname in filenames:
            if fname.endswith(".py"):
                files.append(os.path.join(root, fname).replace("\\", "/"))
    return files


# ╔════════════════════════════════════════════════╗
# ║ SECTION: API – Save File                       ║
# ╚════════════════════════════════════════════════╝
@auto_model
@auto_route
@auto_logic
@router.post("/api/save")
def save_file(data: dict):
    filename = data.get("filename")
    content = data.get("content")
    path = BASE_DIR / filename

    try:
        if path.exists():
            history[filename] = path.read_text(encoding="utf-8")
        path.write_text(content, encoding="utf-8")
        return {"success": True}
    except Exception as e:
        return {"success": False, "message": str(e)}


# ╔════════════════════════════════════════════════╗
# ║ SECTION: API – Merge Patch                     ║
# ╚════════════════════════════════════════════════╝
@auto_model
@auto_route
@auto_logic
@router.post("/api/merge")
def merge_patch(data: dict):
    filename = data.get("filename")
    patch = data.get("patch")
    path = BASE_DIR / filename

    try:
        original = path.read_text(encoding="utf-8")
        history[filename] = original
        new_content = original + "\n" + patch
        path.write_text(new_content, encoding="utf-8")
        return {"success": True, "content": new_content}
    except Exception as e:
        return {"success": False, "message": str(e)}


# ╔════════════════════════════════════════════════╗
# ║ SECTION: API – Undo Changes                    ║
# ╚════════════════════════════════════════════════╝
@auto_model
@auto_route
@auto_logic
@router.get("/api/undo")
def undo_file(file: str):
    if file not in history:
        return {"success": False, "message": "No undo available"}
    try:
        Path(BASE_DIR / file).write_text(history[file], encoding="utf-8")
        return {"success": True, "content": history[file]}
    except Exception as e:
        return {"success": False, "message": str(e)}


# ╔════════════════════════════════════════════════╗
# ║ SECTION: API – Save to Original                ║
# ╚════════════════════════════════════════════════╝
@auto_model
@auto_route
@auto_logic
@router.post("/api/save-to-original")
def save_to_original(data: dict):
    filename = data.get("filename")
    output_code = data.get("output_code")
    path = BASE_DIR / filename

    try:
        if path.exists():
            history[filename] = path.read_text(encoding="utf-8")
        path.write_text(output_code, encoding="utf-8")
        return {"success": True, "message": "File saved successfully!"}
    except Exception as e:
        return {"success": False, "message": str(e)}
