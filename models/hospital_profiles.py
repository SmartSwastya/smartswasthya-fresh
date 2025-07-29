from __future__ import annotations
from tools.obvious_router import auto_model
#region auto_model
# ============================================
from sqlalchemy.sql import func
# ðŸ¥ HOSPITAL PROFILES MODEL
# ============================================

from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base

if TYPE_CHECKING:
    from models.users import User
    # @auto_model
class HospitalProfile(Base):
    __tablename__ = "hospital_profiles"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    hospital_name = Column(String(100))
    registration_number = Column(String(50))
    contact_number = Column(String(20))
    address = Column(String(255))

    user = relationship("User", back_populates="hospital_profile")






