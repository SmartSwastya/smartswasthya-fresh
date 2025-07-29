# route/partner/partner_dashboard.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/partner/dashboard")
def get_partner_dashboard():
    return JSONResponse(content={"partners": ["Pharmacy", "Lab", "Doctor"], "pending_requests": 2})
