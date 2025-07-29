# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_logic
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from tools.obvious_router import auto_logic
from handler import auto_logic
from handler import auto_route
from handler import auto_model
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.otp_sessions import OTPSession
from schemas.sms_otp import SendSMSOTPRequest, VerifySMSOTPRequest
from tools.smart_logger import SmartLogger

logger = SmartLogger("SMSOTP")
# @odil_trace(run=True, apply=True)

# @auto_logic
@auto_model
@auto_route
@auto_logic
def run():
    logger.info("Running logic: sms_otp_logic.run()")
    from database import SessionLocal
    db = SessionLocal()
    try:
        dummy_request = SendSMSOTPRequest(phone="+911234567890")
        result = send_sms_otp_logic(db, dummy_request)
        logger.info("SMS OTP sent")
        return result
    except Exception as e:
        logger.error(f"Run error: {str(e)}")
        return {"status": "error", "message": str(e)}

@auto_model
@auto_route
@auto_logic
def apply():
    logger.info("Running logic: sms_otp_logic.apply()")
    from database import SessionLocal
    db = SessionLocal()
    try:
        dummy_request = VerifySMSOTPRequest(phone="+911234567890", otp="123456")
        result = verify_sms_otp_logic(db, dummy_request)
        logger.info("SMS OTP verification logic triggered")
        return result
    except Exception as e:
        logger.error(f"Apply error: {str(e)}")
        return {"status": "error", "message": str(e)}

# Existing logic assumed to be defined below:
@auto_model
@auto_route
@auto_logic
def send_sms_otp_logic(db: Session, request: SendSMSOTPRequest):
    otp = "123456"
    new_session = OTPSession(phone=request.phone, otp=otp, created_at=datetime.utcnow())
    db.add(new_session)
    db.commit()
    return {"message": f"📲 OTP sent to {request.phone}", "otp": otp}

@auto_model
@auto_route
@auto_logic
def verify_sms_otp_logic(db: Session, request: VerifySMSOTPRequest):
    session = db.query(OTPSession).filter(
        OTPSession.phone == request.phone,
        OTPSession.otp == request.otp
    ).first()

    if session:
        db.delete(session)
        db.commit()
        return {"message": "✅ Phone verified successfully"}

    raise HTTPException(status_code=400, detail="❌ Invalid OTP")

