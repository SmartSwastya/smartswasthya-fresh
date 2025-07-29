# route/pharmacy/pharmacy_inventory.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/pharmacy/inventory")
def get_pharmacy_inventory():
    return JSONResponse(content={"medicines": ["Paracetamol", "Amoxicillin", "Azithromycin"]})
