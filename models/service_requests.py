from models.base import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING
from tools.obvious_router import auto_model

if TYPE_CHECKING:
    from models.users import User
    # @auto_model
class ServiceRequest(Base):
    __tablename__ = "service_requests"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    service_type = Column(String(50))  # lab, ambulance, homecare, etc.
    details = Column(Text)
    requested_at = Column(DateTime)
    status = Column(String(20))  # pending, approved, completed, rejected

    user = relationship("User", back_populates="service_requests")






