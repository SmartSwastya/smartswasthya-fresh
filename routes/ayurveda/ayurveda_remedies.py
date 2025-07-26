# routes/ayurveda/ayurveda_remedies.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/ayurveda/remedies")
def list_ayurveda_remedies():
    return JSONResponse(content={"remedies": ["Triphala", "Ashwagandha", "Tulsi"]})
