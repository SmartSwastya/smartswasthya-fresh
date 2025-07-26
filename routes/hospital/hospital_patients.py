# route/hospital/hospital_patients.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/hospital/patients")
def list_admitted_patients():
    return JSONResponse(content={"patients": ["P001", "P002", "P003"]})
