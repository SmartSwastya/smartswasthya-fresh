from tools.obvious_router import auto_model
#region auto_model
# ============================================
from sqlalchemy.sql import func
# ðŸ” OTP SESSIONS MODEL
# ============================================

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.users import User
    # @auto_model
class OTPSession(Base):
    __tablename__ = "otp_sessions"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    mobile = Column(String, nullable=False)
    email = Column(String, nullable=True)
    otp_code = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_verified = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="otp_sessions")






