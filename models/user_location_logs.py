from tools.obvious_router import auto_model
#region auto_model
# ============================================
from sqlalchemy.sql import func
# ðŸ“ USER LOCATION LOGS MODEL
# ============================================

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.users import User
    # @auto_model
class UserLocationLog(Base):
    __tablename__ = "user_location_logs"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    latitude = Column(Float)
    longitude = Column(Float)
    accuracy = Column(Float)
    timestamp = Column(DateTime)

    user = relationship("User", back_populates="location_logs")






