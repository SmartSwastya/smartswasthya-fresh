# route/pharmacy/pharmacy_orders.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/pharmacy/order")
def place_pharmacy_order(order_id: str):
    return JSONResponse(content={"order_id": order_id, "status": "confirmed"})
