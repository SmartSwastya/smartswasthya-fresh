from tools.obvious_router import auto_model
#region auto_model
# ============================================
from sqlalchemy.sql import func
# ðŸ“‚ LOGIN SESSIONS MODEL
# ============================================

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.users import User
    # @auto_model
class LoginSession(Base):
    __tablename__ = "login_sessions"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    session_token = Column(String)
    created_at = Column(DateTime)
    expired_at = Column(DateTime)

    user = relationship("User", back_populates="login_sessions")






