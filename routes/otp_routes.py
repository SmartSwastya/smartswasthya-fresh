# ✅ OTP Routes – Fast2SMS Enabled
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from database import get_db
from models.users import User
from utils.fast2sms_otp_handler import send_otp, verify_otp

router = APIRouter()

# ✅ 1. Send OTP – Fast2SMS
@router.get("/otp")
async def route_send_otp(request: Request, mobile: str, name: str = "Smart User", gender: str = "other", db: Session = Depends(get_db)):
    result = send_otp(mobile=mobile, name=name, db=db)
    return JSONResponse(content=result)

# ✅ 2. Verify OTP
@router.post("/verify")
async def route_verify_otp(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    mobile = data.get("mobile")
    otp = data.get("otp")
    if not mobile or not otp:
        return JSONResponse(content={"status": "error", "message": "Missing mobile or otp"}, status_code=400)
    result = verify_otp(mobile=mobile, otp=otp, db=db)
    return JSONResponse(content=result)

# ✅ 3. Check if mobile already exists
@router.get("/check-mobile-exists")
async def route_check_mobile_exists(mobile: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.mobile == mobile).first()

    if user:
        return {"status": "existing"}
    return {"status": "create"}
