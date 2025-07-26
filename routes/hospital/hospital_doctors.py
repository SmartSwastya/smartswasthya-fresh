# route/hospital/hospital_doctors.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/hospital/doctors")
def list_hospital_doctors():
    return JSONResponse(content={"doctors": ["Dr. A", "Dr. B", "Dr. C"]})
