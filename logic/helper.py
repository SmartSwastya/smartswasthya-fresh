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
#region auto_logic
# ======================================
# 📁 logic/helper.py
# ======================================

from tools.smart_logger import SmartLogger
from sqlalchemy.orm import Session

logger = SmartLogger("Helper")
# @odil_trace(run=True, apply=True)

@auto_model
@auto_route
@auto_logic
def run(db: Session, action: str = "ping") -> dict:
    logger.info(f"Running helper.run() with action: {action}")
    
    if action == "audit":
        # Future: audit engine trigger
        return {"status": "ok", "audit": True}
    elif action == "ping":
        return {"status": "pong", "message": "System responsive"}
    else:
        return {"status": "unknown", "action": action}


@auto_model
@auto_route
@auto_logic
def apply(db: Session, model: str = "User", field: str = None, value: str = None) -> dict:
    logger.info(f"Applying update on {model}: {field} = {value}")
    
    # Future: actual DB patch via reflection
    if not field or not value:
        return {"status": "error", "message": "Missing field or value"}
    
    return {
        "status": "applied",
        "model": model,
        "field": field,
        "value": value
    }

# ⬇️ Add this to logic/helper.py (anywhere appropriate)
from models.users import User  # if not already imported

@auto_model
@auto_route
@auto_logic
def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

