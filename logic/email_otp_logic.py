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
# 📁 FILE: logic/email_otp_logic.py

from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.otp_sessions import OTPSession
from schemas.email_otp import SendEmailOTPRequest, VerifyEmailOTPRequest
import random
import smtplib
from email.mime.text import MIMEText

from tools.smart_logger import SmartLogger
logger = SmartLogger("EmailOTP")
# @odil_trace(run=True, apply=True)

# @auto_logic
@auto_model
@auto_route
@auto_logic
def run():
    logger.info("Running logic: email_otp_logic.run()")
    from database import SessionLocal
    from schemas.email_otp import SendEmailOTPRequest
    db = SessionLocal()
    try:
        dummy_request = SendEmailOTPRequest(email="testuser@example.com")
        result = send_email_otp_logic(db, dummy_request)
        logger.info("OTP send logic triggered successfully")
        return result
    except Exception as e:
        logger.error(f"Run error: {str(e)}")
        return {"status": "error", "message": str(e)}

@auto_model
@auto_route
@auto_logic
def apply():
    logger.info("Running logic: email_otp_logic.apply()")
    from database import SessionLocal
    from schemas.email_otp import VerifyEmailOTPRequest
    db = SessionLocal()
    try:
        dummy_request = VerifyEmailOTPRequest(email="testuser@example.com", otp="123456")
        result = verify_email_otp_logic(db, dummy_request)
        logger.info("OTP verification logic triggered")
        return result
    except Exception as e:
        logger.error(f"Apply error: {str(e)}")
        return {"status": "error", "message": str(e)}

# ─────────────────────────────────────────────────────────
# ✅ NEWLY MERGED FUNCTION (from email_verification.py)
# ─────────────────────────────────────────────────────────
@auto_model
@auto_route
@auto_logic
def can_resend_otp(session: OTPSession) -> bool:
    return datetime.utcnow() - session.created_at > timedelta(seconds=60)

# ─────────────────────────────────────────────────────────
# ✅ EXISTING LOGIC — send and verify
# ─────────────────────────────────────────────────────────
@auto_model
@auto_route
@auto_logic
def send_email_otp_logic(db: Session, request: SendEmailOTPRequest):
    existing_session = db.query(OTPSession).filter(OTPSession.email == request.email).first()

    if existing_session:
        if not can_resend_otp(existing_session):
            raise HTTPException(status_code=400, detail="⏳ Wait 60 seconds before resending OTP")
        db.delete(existing_session)
        db.commit()

    otp = str(random.randint(100000, 999999))
    new_session = OTPSession(email=request.email, otp=otp, created_at=datetime.utcnow())
    db.add(new_session)
    db.commit()

    subject = "📩 Your Smart Swasthya Seva Email OTP"
    body = f"Your OTP is: {otp}"
    send_email(request.email, subject, body)

    return {"message": "📩 OTP sent successfully"}

@auto_model
@auto_route
@auto_logic
def verify_email_otp_logic(db: Session, request: VerifyEmailOTPRequest):
    session = db.query(OTPSession).filter(
        OTPSession.email == request.email,
        OTPSession.otp == request.otp
    ).first()

    if session:
        db.delete(session)
        db.commit()
        return {"message": "✅ Email verified successfully"}

    raise HTTPException(status_code=400, detail="❌ Invalid OTP")

@auto_model
@auto_route
@auto_logic
def send_email(to_email: str, subject: str, body: str):
    sender_email = "noreply@smartswasthyaseva.com"
    smtp_server = "localhost"
    smtp_port = 25

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.send_message(msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"📡 Failed to send email: {str(e)}")

