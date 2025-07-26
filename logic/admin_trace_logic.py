# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_logic
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from tools.obvious_router import auto_logic
# 📁 FILE: logic/admin_trace_logic.py
from handler import auto_logic
from handler import auto_route
from handler import auto_model
from tools.smart_logger import SmartLogger
logger = SmartLogger("AdminTrace")

# 🔒 In-memory permission store (non-persistent)
session_permissions: dict[int, dict[str, bool]] = {}
# @odil_trace(run=True, apply=True)

# @auto_logic
@auto_model
@auto_route
@auto_logic
def run():
    logger.info("Running admin_trace_logic.run() — listing active devs with permissions")
    return {
        "status": "success",
        "developers": get_active_developers_with_permissions()
    }

@auto_model
@auto_route
@auto_logic
def apply():
    logger.info("Running admin_trace_logic.apply() — No write actions implemented")
    return {
        "status": "noop",
        "message": "No changes applied via admin_trace_logic.apply()"
    }

# ✅ Set a specific permission toggle for a user session
@auto_model
@auto_route
@auto_logic
def set_permission(user_id: int, key: str, value: bool) -> None:
    if user_id not in session_permissions:
        session_permissions[user_id] = {}
    session_permissions[user_id][key] = value

# 📤 Get all permissions for a user session
@auto_model
@auto_route
@auto_logic
def get_permissions(user_id: int) -> dict[str, bool]:
    return session_permissions.get(user_id, {
        "core_file_access": False,
        "manual_trace": False,
        "db_override": False,
    })

# ❌ Reset permissions when session ends (optional, can call on logout)
@auto_model
@auto_route
@auto_logic
def reset_permissions(user_id: int) -> None:
    session_permissions.pop(user_id, None)

from tools.auth import decode_token_safely as decode_token
from models.users import User
from database import SessionLocal

# 🧠 Get session-wise active developers (mock example)
@auto_model
@auto_route
@auto_logic
def get_active_developers_with_permissions():
    db = SessionLocal()
    users = db.query(User).filter(User.is_active == True).all()
    return [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "is_admin": u.is_admin,
            "is_verified": u.is_verified,
            "permissions": get_permissions(u.id)
        } for u in users
    ]

