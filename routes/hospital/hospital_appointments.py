# route/hospital/hospital_appointments.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/hospital/appointments/{patient_id}")
def get_appointments(patient_id: int):
    return JSONResponse(content={"patient_id": patient_id, "appointments": ["10 AM", "2 PM"]})
