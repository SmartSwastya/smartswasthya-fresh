# ╔════════════════════════════════════════════════╗
# ║ FILE: routes/dev/api_routes.py                 ║
# ║ PURPOSE: Dev API Monitor                       ║
# ╚════════════════════════════════════════════════╝

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import os
import requests

from tools.obvious_router import auto_route, auto_logic

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Router Init                           ║
# ╚════════════════════════════════════════════════╝
router = APIRouter(prefix="/dev/api", tags=["Dev API Monitor"])
templates = Jinja2Templates(directory="templates")

# ╔════════════════════════════════════════════════╗
# ║ ROUTE: Dev API Monitor Dashboard               ║
# ╚════════════════════════════════════════════════╝
@auto_route
@auto_logic
@router.get("/api")
async def show_api_page(request: Request):
    return templates.TemplateResponse("dev/api/api.html", {"request": request})

# ╔════════════════════════════════════════════════╗
# ║ ROUTE: External Service Test                   ║
# ╚════════════════════════════════════════════════╝
@auto_route
@auto_logic
@router.get("/test/{service}")
async def test_service(service: str):
    try:
        if service == "fast2sms":
            key = os.getenv("FAST2SMS_API_KEY")
            sender_id = os.getenv("FAST2SMS_SENDER_ID")
            url = f"https://www.fast2sms.com/dev/bulkV2?authorization={key}&route=otp&variables_values=123456&flash=0&numbers=9999999999&sender_id={sender_id}"
            headers = { "cache-control": "no-cache" }
            r = requests.get(url, headers=headers, timeout=5)
            return JSONResponse(content={"ok": r.status_code == 200, "response": r.text})

        elif service == "surepass":
            key = os.getenv("SUREPASS_API_KEY")
            url = "https://kyc-api.surepass.io/api/v1/health"
            headers = { "Authorization": f"Bearer {key}" }
            r = requests.get(url, headers=headers, timeout=5)
            return JSONResponse(content={"ok": r.status_code == 200, "response": r.text})

        else:
            return JSONResponse(status_code=400, content={"ok": False, "message": "Unknown service"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"ok": False, "message": str(e)})

# ╔════════════════════════════════════════════════╗
# ║ ROUTE: Fit Status Checker                      ║
# ╚════════════════════════════════════════════════╝
@auto_route
@auto_logic
@router.get("/status/fit")
async def check_fit():
    return JSONResponse(content={"ok": False, "message": "Google Fit not configured"})

# ╔════════════════════════════════════════════════╗
# ║ ROUTE: OAuth Status Checker                    ║
# ╚════════════════════════════════════════════════╝
@auto_route
@auto_logic
@router.get("/status/oauth")
async def check_oauth():
    return JSONResponse(content={"ok": False, "message": "OAuth not configured"})
