# ✅ FILE: schemas/sms_otp.py
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from pydantic import BaseModel, Field

class SendSMSOTPRequest(BaseModel):
    mobile: str = Field(..., min_length=10, max_length=10)
    name: str
    gender: str = "other"

class VerifySMSOTPRequest(BaseModel):
    mobile: str = Field(..., min_length=10, max_length=10)
    otp: str = Field(..., min_length=6, max_length=6)
    name: str
    email: str = ""
    password: str
    gender: str = "other"

def __trace_marker__(): pass
