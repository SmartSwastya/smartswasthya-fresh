# routes/corporate/corporate_wellness.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/corporate/wellness")
def get_corporate_wellness_programs():
    return JSONResponse(content={"programs": ["Yoga", "Health Checkup", "Diet Counselling"]})
