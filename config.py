# ✅ config.py — Compatible with .env and Pydantic v2
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 🧭 Execution Mode
    IS_DOCKER: int
    LOCAL_DIR: str

    # 🔐 Security
    SECRET_KEY: str
    JWT_SECRET: str  # ✅ Required for token_logic

    # 🧹 Auto Cleanup
    CLEANUP_DAYS: int

    # 🚀 App Boot Mode
    APP_MODE: str

    # 📦 Database
    DATABASE_URL: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # 🔗 Redis + Celery
    REDIS_URL: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # 📬 Mail
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_USE_TLS: bool
    MAIL_USE_SSL: bool

    # ☎️ Fast2SMS
    FAST2SMS_KEY: str
    FAST2SMS_SENDER_ID: str
    FAST2SMS_TEMPLATE_ID: str
    FAST2SMS_TEST_NUMBER: str

    # 🔐 Google Client
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    # 🌐 Google OAuth / Fit / Geo
    GOOGLE_OAUTH_CLIENT_ID: str
    GOOGLE_OAUTH_CLIENT_SECRET: str
    GOOGLE_OAUTH_REDIRECT_URI: str
    GOOGLE_FIT_CLIENT_ID: str
    GOOGLE_FIT_CLIENT_SECRET: str
    GOOGLE_FIT_API_KEY: str
    GOOGLE_GEO_API_KEY: str

    # 🔍 Monitoring
    SENTRY_DSN: str

    # ✅ Surepass KYC
    SUREPASS_BASE_URL: str
    SUREPASS_BEARER_TOKEN: str
    SUREPASS_AADHAAR_TEST: str

    # 🔐 SSH (optional)
    SSH_PORT: int
    SSH_USERNAME: str
    SSH_HOST: str
    SSH_PASSWORD: str
    SSH_PRIVATE_KEY_PATH: str

    # ⚙️ Build
    FLASK_DEBUG: int
    GOOGLE_APPLICATION_CREDENTIALS: str
    SERVER_DIR: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

# 🟢 Instantiate settings object
settings = Settings()
