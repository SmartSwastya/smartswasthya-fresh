# route/hospital/hospital_discharge.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/hospital/discharge")
def discharge_patient(patient_id: int):
    return JSONResponse(content={"status": "discharged", "patient_id": patient_id})
