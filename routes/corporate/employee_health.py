# routes/corporate/employee_health.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/corporate/employee/health/{emp_id}")
def get_employee_health(emp_id: int):
    return JSONResponse(content={"employee_id": emp_id, "status": "healthy"})
