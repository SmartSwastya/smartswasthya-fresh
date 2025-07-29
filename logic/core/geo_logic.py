# root/smartswasthya/logic/core/geo_logic.py

async def smart_service_search(query: str, latitude: float, longitude: float):
    return [
        {"name": "Local Pharmacy", "distance_km": 1.2, "type": query},
        {"name": "Care Meds", "distance_km": 2.5, "type": query}
    ]

async def find_nearby_ambulances(lat: float, lon: float):
    return [
        {"id": "amb_101", "lat": lat + 0.01, "lon": lon + 0.01},
        {"id": "amb_102", "lat": lat + 0.02, "lon": lon + 0.01},
        {"id": "amb_103", "lat": lat - 0.01, "lon": lon - 0.02},
    ]

async def broadcast_emergency_to(ambulance_list: list):
    for amb in ambulance_list:
        print(f"🚨 Alert sent to Ambulance: {amb['id']}")
