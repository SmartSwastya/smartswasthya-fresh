# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# smartswasthya/compatibility/moderator.py

"""
Legacy Moderator Compatibility Adapter
Handles: SmartUser → User adapter fallback
"""

from tools.smart_logger import SmartLogger
logger = SmartLogger("moderator")

@auto_model
@auto_route
@auto_logic
def adapt_moderator_data(raw_data):
    """
    Accepts old format and returns standardized user dict
    """
    if "moderator_id" in raw_data:
        logger.debug("Legacy moderator format detected")
        return {
            "id": raw_data["moderator_id"],
            "name": raw_data.get("name", "Unknown"),
            "email": raw_data.get("email"),
            "role": "moderator"
        }
    return raw_data

