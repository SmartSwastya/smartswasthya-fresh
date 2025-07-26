# ────────────────────────────────────────────────────────────────
# 📁 FILE: routes/dev/token_routes.py
# 📌 PURPOSE: Token API — create dev/test tokens
# ────────────────────────────────────────────────────────────────
# 📁 routes/dev/token_routes.py

from fastapi import APIRouter, Request

from tools.smart_template import templates
from tools.obvious_router import auto_route
from handler import auto_model, auto_logic

from logic.dev.token_logic import (
    create_token_logic,
    verify_token_post_logic,
    verify_token_query_logic,
    blacklist_token_logic,
    expire_token_logic,
    get_all_tokens_logic,
    list_tokens_logic
)

router = APIRouter(prefix="/dev/token", tags=["Token"])


# ╔════════════════════════════════════════════════╗
# ║ SECTION: Token UI Page                         ║
# ╚════════════════════════════════════════════════╝
@auto_model
@auto_route
@auto_logic
@router.get("/token")
def show_token_page(request: Request):
    return templates.TemplateResponse("token.html", {"request": request})


# ╔════════════════════════════════════════════════╗
# ║ SECTION: Token APIs                            ║
# ╚════════════════════════════════════════════════╝
@auto_model
@auto_route
@auto_logic
@router.post("/api/token/create")
async def create_token(request: Request):
    return await create_token_logic(request)


@auto_model
@auto_route
@auto_logic
@router.post("/api/token/blacklist")
async def blacklist_token(request: Request):
    return await blacklist_token_logic(request)


@auto_model
@auto_route
@auto_logic
@router.post("/api/token/expire")
async def expire_token(request: Request):
    return await expire_token_logic(request)


@auto_model
@auto_route
@auto_logic
@router.get("/api/tokens")
def get_all_tokens():
    return get_all_tokens_logic()


@auto_model
@auto_route
@auto_logic
@router.get("/tokens")
def list_tokens(request: Request):
    return list_tokens_logic(request)
