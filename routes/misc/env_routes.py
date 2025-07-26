# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import os
from tools.smart_logger import SmartLogger
from handler import auto_model, auto_logic, auto_route

router = APIRouter(prefix="/dev/env", tags=["Environment"])
templates = Jinja2Templates(directory="templates")
logger = SmartLogger("env_routes")

@router.get("")
@auto_model
@auto_route
@auto_logic
def render_env_view(request: Request):
    return templates.TemplateResponse("dev/env/env.html", {"request": request})

@router.get("/api/vars")
@auto_model
@auto_route
@auto_logic
def get_env_variables():
    keys_to_include = [
        "DB_URL", "REDIS_URL", "SECRET_KEY",
        "GOOGLE_CLIENT_ID", "SUREPASS_API_KEY",
        "FAST2SMS_API_KEY", "ENV", "DEBUG"
    ]
    result = {key: os.getenv(key, "🔒 hidden") for key in keys_to_include}
    logger.debug("Fetched environment variables.")
    return JSONResponse(content=result)

@router.get("/api/restart")
@auto_model
@auto_route
@auto_logic
def restart_server():
    logger.warning("Restart triggered (simulation only).")
    return JSONResponse(content={"message": "🔁 Restart simulated — requires Docker or process manager."})

@router.get("/api/clear")
@auto_model
@auto_route
@auto_logic
def clear_env_cache():
    logger.info("Environment cache cleared (simulated).")
    return JSONResponse(content={"message": "🧹 Environment cache cleared"})

@router.get("/api/mode")
@auto_model
@auto_route
@auto_logic
def get_env_mode():
    env = os.getenv("ENV", "development")
    logger.debug(f"ENV mode: {env}")
    return JSONResponse(content={"message": f"Current ENV mode is: {env}"})
