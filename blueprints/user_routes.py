# ╔═══════════════════════════════════════════════════════════════════════╗
# ║               SMART SWASTHYA – USER MODULE BLUEPRINT                 ║
#region auto_route
# ║      Smart User Profile, Verification, Age, Location, etc.           ║
# ╚═══════════════════════════════════════════════════════════════════════╝

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter
from tools.smart_marker_injector import auto_route
from tools.obvious_router import auto_route

user_router = APIRouter(prefix="/smart-user", tags=["Smart User"])

# 🔗 Profile & Verification Routes
user_router.include_router(profile_router)
user_router.include_router(user_profile_router)
user_router.include_router(smart_user_router)

