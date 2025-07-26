# 📦 SCHEMAS — EMAIL OTP REQUEST SCHEMAS
# --------------------------------------
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from pydantic import BaseModel, EmailStr

class SendEmailOTPRequest(BaseModel):
    email: EmailStr

class VerifyEmailOTPRequest(BaseModel):
    email: EmailStr
    otp: str

def __trace_marker__(): pass
