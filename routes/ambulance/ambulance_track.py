# routes/ambulance/ambulance_track.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/ambulance/track/{ambulance_id}")
def track_ambulance(ambulance_id: int):
    return JSONResponse(content={"ambulance_id": ambulance_id, "status": "en route", "eta": "7 mins"})
