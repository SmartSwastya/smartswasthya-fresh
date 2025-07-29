# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse  # ✅ Added for favicon
from dotenv import load_dotenv

from tools.smart_logger import SmartLogger
from tools.timezone_utils import now_ist
from registry.app_registry import setup_app  # ✅ Unified router registry
from tools.smart_template import templates

# ╔════════════════════════════════════════════════╗
# ║ SECTION: System Boot                           ║
# ╚════════════════════════════════════════════════╝
now_ist()
load_dotenv()
logger = SmartLogger("MainApp")

# ╔════════════════════════════════════════════════╗
# ║ SECTION: FastAPI App Initialization            ║
# ╚════════════════════════════════════════════════╝
app = FastAPI(title="Smart Swasthya Seva")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Static Files + Templates              ║
# ╚════════════════════════════════════════════════╝
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ Serve favicon.ico properly for browsers
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

# ╔════════════════════════════════════════════════╗
# ║ SECTION: CORS Middleware                       ║
# ╚════════════════════════════════════════════════╝
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Full System Autoregister              ║
# ╚════════════════════════════════════════════════╝
setup_app(app)  # ✅ All logic, route, blueprint, templates bound

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Dev Launch Entry (Optional)           ║
# ╚════════════════════════════════════════════════╝
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
