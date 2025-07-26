# 📁 File: smartswasthya/abdm/sandbox_config.py

# ABDM Sandbox Gateway Constants (No interpreter dependencies)

ABDM_GATEWAY_BASE = "https://dev.abdm.gov.in/gateway/v0.5"

ABHA_APIS = {
    "generate_mobile_otp": ABDM_GATEWAY_BASE + "/registration/mobile/generateOtp",
    "verify_mobile_otp": ABDM_GATEWAY_BASE + "/registration/mobile/verifyOtp",
    "create_abha_address": ABDM_GATEWAY_BASE + "/phr-address"
}

CONSENT_APIS = {
    "request": ABDM_GATEWAY_BASE + "/consent-requests/init",
    "status": ABDM_GATEWAY_BASE + "/consent-requests/status",
    "on_notify": "/api/abdm/on-notify"  # Local route for webhook
}

# Static Auth Headers (will be extended by auth token at runtime)
SANDBOX_HEADERS = {
    "Content-Type": "application/json",
    "X-CM-ID": "sbx"  # Sandbox Client ID
}

# JWT Token Placeholder — to be loaded via config/env manager later
SANDBOX_AUTH_TOKEN = "Bearer YOUR_SANDBOX_JWT_TOKEN"
