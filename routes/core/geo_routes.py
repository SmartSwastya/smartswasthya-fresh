# root/smartswasthya/routes/core/geo_routes.py

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from logic.core.geo_logic import (
    smart_service_search,
    find_nearby_ambulances,
    broadcast_emergency_to
)

# ✅ Add this line for SmartEngine route registration
from handler import auto_route

router = APIRouter()

# ------------------------------
# 📍 SEARCH NEARBY HOOK
# ------------------------------
@auto_route
@router.post("/search-nearby")
async def search_nearby(request: Request):
    data = await request.json()
    query = data.get("query")
    lat = data.get("latitude")
    lon = data.get("longitude")

    if not (query and lat and lon):
        return JSONResponse(status_code=400, content={"status": "error", "message": "Missing data"})

    results = await smart_service_search(query, lat, lon)
    return {"status": "success", "results": results}


# ------------------------------
# 🚑 EMERGENCY REQUEST HOOK
# ------------------------------
@auto_route
@router.post("/emergency-request")
async def emergency_request(request: Request):
    data = await request.json()
    lat = data.get("latitude")
    lon = data.get("longitude")
    user_id = data.get("user_id")  # optional

    if not (lat and lon):
        return JSONResponse(status_code=400, content={"status": "error", "message": "Missing location"})

    ambulances = await find_nearby_ambulances(lat, lon)
    await broadcast_emergency_to(ambulances)

    return {"status": "alert_sent", "options": ambulances}
