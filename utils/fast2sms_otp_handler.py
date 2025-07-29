import os
import random
import datetime
import requests
from sqlalchemy.orm import Session
from typing import Literal

from models.otp_sessions import OTPSession
from dlt_templates.dlt_templates import templates


# ----------------------- CORE SEND -----------------------

def send_otp(
    mobile: str,
    db: Session,
    name: str = "Smart User",
    template_key: Literal["RegOTP", "ForgotPassword"] = "RegOTP"
) -> dict:
    otp = str(random.randint(100000, 999999))
    template = templates.get(template_key)

    if not template:
        return {"status": "error", "message": f"Template '{template_key}' not found."}

    for field in ["api_key", "sender_id", "template_id", "sms_template"]:
        if field not in template:
            return {"status": "error", "message": f"Template missing field: {field}"}

    payload = {
        "authorization": template["api_key"],
        "route": "dlt",
        "sender_id": template["sender_id"],
        "message": template["template_id"],
        "variables_values": f"{name}|{otp}",
        "numbers": mobile,
        "flash": "0"
    }

    try:
        response = requests.get("https://www.fast2sms.com/dev/bulkV2", params=payload)
        data = response.json()

        if data.get("return") is True:
            otp_entry = OTPSession(
                mobile=mobile, 
                otp_code=otp,
                expires_at=datetime.datetime.utcnow() + datetime.timedelta(minutes=5)  # Fix: Set expires_at
            )
            db.add(otp_entry)
            db.commit()
            _log_otp_sent(mobile, otp)
            print(f"[DEV] OTP for {mobile} → {otp}", flush=True)
            return {"status": "sent", "otp": otp}
        else:
            error = data.get("message", "Unknown error")
            _log_otp_failure(mobile, error)
            print(f"[DEV] OTP Response: {data}", flush=True)
            return {"status": "failed", "message": error}

    except Exception as e:
        _log_otp_failure(mobile, str(e))
        print(f"[DEV] OTP Send Error: {e}", flush=True)
        return {"status": "error", "message": str(e)}


# ----------------------- CORE VERIFY -----------------------

def verify_otp(mobile: str, otp: str, db: Session) -> dict:
    entry = (
        db.query(OTPSession)
        .filter_by(mobile=mobile, otp_code=otp, is_verified=False)
        .order_by(OTPSession.created_at.desc())
        .first()
    )

    if not entry:
        return {"status": "invalid", "reason": "OTP incorrect or expired"}

    if datetime.datetime.utcnow() > entry.expires_at:
        return {"status": "expired", "reason": "OTP expired"}

    entry.is_verified = True
    db.commit()
    _log_otp_verified(mobile)
    return {"status": "verified"}


# ----------------------- FORGOT OTP -----------------------

def send_forgot_otp(mobile: str, db: Session, name: str = "Smart User") -> dict:
    return send_otp(mobile, db, name, template_key="ForgotPassword")


# ----------------------- LOGGING -----------------------

def _log_otp_sent(mobile: str, otp: str):
    _ensure_logs()
    with open("logs/otp.log", "a") as f:
        f.write(f"[{_now()}] [OTP] {mobile} → {otp} ✅ sent\n")

def _log_otp_verified(mobile: str):
    _ensure_logs()
    with open("logs/otp.log", "a") as f:
        f.write(f"[{_now()}] [VERIFIED] OTP for {mobile} ✅ used successfully\n")

def _log_otp_failure(mobile: str, error: str):
    _ensure_logs()
    with open("logs/otp_error.log", "a") as f:
        f.write(f"[{_now()}] [FAILED] OTP for {mobile} ❌ {error}\n")

def _ensure_logs():
    os.makedirs("logs", exist_ok=True)

def _now() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")