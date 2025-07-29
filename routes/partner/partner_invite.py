# routes/partner/partner_invite.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/partner/invite")
def send_partner_invite(email: str):
    return JSONResponse(content={"status": "invite_sent", "email": email})
