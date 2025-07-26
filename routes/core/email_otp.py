# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# ⛳ ROUTES — EMAIL OTP ROUTES
# --------------------------------------
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.email_otp import SendEmailOTPRequest, VerifyEmailOTPRequest
from logic.email_otp_logic import send_email_otp_logic, verify_email_otp_logic
from database import get_db
from tools.smart_marker_injector import auto_route
from tools.obvious_router import auto_route

router = APIRouter()

# @auto_route
@router.post("/send-email-otp", operation_id="post_send-email-otp")
@auto_model
@auto_route
@auto_logic
def send_email_otp(data: SendEmailOTPRequest, db: Session = Depends(get_db)):
    return send_email_otp_logic(db, data)

@router.post("/verify-email-otp", operation_id="post_verify-email-otp")
@auto_model
@auto_route
@auto_logic
def verify_email_otp(data: VerifyEmailOTPRequest, db: Session = Depends(get_db)):
    return verify_email_otp_logic(db, data)


