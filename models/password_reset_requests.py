from tools.obvious_router import auto_model
#region auto_model
# ============================================
from sqlalchemy.sql import func
# ðŸ”‘ PASSWORD RESET REQUESTS MODEL
# ============================================

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.users import User
    # @auto_model
class PasswordResetRequest(Base):
    __tablename__ = "password_reset_requests"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    reset_token = Column(String)
    requested_at = Column(DateTime)
    used_at = Column(DateTime)

    user = relationship("User", back_populates="password_resets")






