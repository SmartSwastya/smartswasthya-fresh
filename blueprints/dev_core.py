# blueprints/dev_core.py
# ╔═══════════════════════════════════════════════════════════════════════╗
# ║                SMART SWASTHYA – DEV CORE BLUEPRINT                   ║
# ║       Base-level System Routes: Landing, Awareness, Home etc.        ║
# ╚═══════════════════════════════════════════════════════════════════════╝

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter
from fastapi.responses import HTMLResponse  # ✅ Fix: Ensure HTMLResponse is imported if needed

dev_core_router = APIRouter()

# 🔗 Core System Routes
dev_core_router.include_router(index_router)
dev_core_router.include_router(awareness_router)
dev_core_router.include_router(login_router)
dev_core_router.include_router(signup_router)
