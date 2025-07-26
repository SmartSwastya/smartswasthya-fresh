# route/blood/blood_inventory.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/bloodbank/inventory")
def get_blood_inventory():
    return JSONResponse(content={
        "inventory": {
            "A+": 12,
            "B+": 8,
            "O-": 5,
            "AB+": 3
        }
    })
