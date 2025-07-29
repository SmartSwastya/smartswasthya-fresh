# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# smartswasthya/compatibility/email_verification.py

"""
Legacy Email Compatibility Adapter
Maps older email verification methods to patched system
"""

from tools.smart_logger import SmartLogger
logger = SmartLogger("email_verification")

@auto_model
@auto_route
@auto_logic
def verify_email(email):
    """
    Legacy fallback to mark email as verified if domain trusted
    """
    if email.endswith("@gmail.com"):
        logger.debug(f"Auto-verifying Gmail email: {email}")
        return True
    logger.warning(f"Email {email} not auto-verified (non-Gmail)")
    return False

