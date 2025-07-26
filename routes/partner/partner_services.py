# routes/partner/partner_services.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/partner/services")
def list_partner_services():
    return JSONResponse(content={"services": ["KYC", "Promotion", "Dashboard Access"]})
