# route/blood/blood_requests.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/bloodbank/request")
def request_blood(blood_type: str, units: int):
    return JSONResponse(content={"status": "received", "blood_type": blood_type, "units": units})
