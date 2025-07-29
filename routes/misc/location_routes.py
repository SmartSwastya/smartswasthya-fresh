# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.obvious_router import auto_logic
# smartswasthya/routes/location_routes.py
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from tools.smart_marker_injector import auto_route
from tools.obvious_router import auto_route

router = APIRouter()

# @auto_route
@router.post("/track-location")
# @auto_logic
async def track_location(request: Request):
    try:
        location_data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    latitude = location_data.get("latitude")
    longitude = location_data.get("longitude")

    if latitude is None or longitude is None:
        raise HTTPException(status_code=400, detail="Missing latitude or longitude")

#region auto_route
    print(f"📍 Received Location: Latitude={latitude}, Longitude={longitude}")
    return JSONResponse(content={"latitude": latitude, "longitude": longitude})

