# routes/ayurveda/ayurveda_consult.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/ayurveda/consult")
def ayurveda_consultation_info():
    return JSONResponse(content={"status": "available", "consultants": ["Dr. Ved", "Dr. Sanjeevani"]})
