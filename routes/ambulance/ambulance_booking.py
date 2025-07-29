# routes/ambulance/ambulance_booking.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/ambulance/book")
def book_ambulance(patient_id: int, location: str):
    return JSONResponse(content={"status": "booked", "patient_id": patient_id, "location": location})
