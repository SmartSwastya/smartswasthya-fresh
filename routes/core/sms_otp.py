# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# ✅ FILE: routes/sms_otp.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.sms_otp import SendSMSOTPRequest, VerifySMSOTPRequest
from logic.sms_otp_logic import send_sms_otp_logic, verify_sms_otp_logic
from database import get_db
from tools.smart_marker_injector import auto_route
from tools.obvious_router import auto_route

router = APIRouter(prefix="/sms-otp", tags=["SMS OTP"])

# @auto_route
@router.post("/send", operation_id="post_send")
@auto_model
@auto_route
@auto_logic
def send_sms_otp(data: SendSMSOTPRequest, db: Session = Depends(get_db)):
    result = send_sms_otp_logic(db, data)
    if result["status"] == "failed":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@router.post("/verify", operation_id="post_verify")
@auto_model
@auto_route
@auto_logic
def verify_sms_otp(data: VerifySMSOTPRequest, db: Session = Depends(get_db)):
    result = verify_sms_otp_logic(db, data)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

