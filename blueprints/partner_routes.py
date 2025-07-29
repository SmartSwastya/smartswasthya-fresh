# ╔═══════════════════════════════════════════════════════════════════════╗
# ║             SMART SWASTHYA – SMART PARTNER BLUEPRINT                 ║
#region auto_route
# ║      Upgrade Flow, KYC, Partner Docs, Earnings, Commission           ║
# ╚═══════════════════════════════════════════════════════════════════════╝

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter
from tools.smart_marker_injector import auto_route
from tools.obvious_router import auto_route

partner_router = APIRouter(prefix="/partner", tags=["Smart Partner"])

# 🔗 Upgrade + Verification Routes
partner_router.include_router(core_partner_router)
partner_router.include_router(kyc_router)
partner_router.include_router(docs_router)

