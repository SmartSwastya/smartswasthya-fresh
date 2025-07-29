from models.base import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING
from tools.obvious_router import auto_model

if TYPE_CHECKING:
    from models.users import User
    # @auto_model
class EmergencyAlert(Base):
    __tablename__ = "emergency_alerts"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    alert_type = Column(String(100))  # e.g., "SOS", "Medical", etc.
    alert_message = Column(String(500))
    timestamp = Column(DateTime)

    user = relationship("User", back_populates="emergency_alerts")






