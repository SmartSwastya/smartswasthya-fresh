from __future__ import annotations
from tools.obvious_router import auto_model
#region auto_model
# ============================================
from sqlalchemy.sql import func
# ðŸ‘¨â€âš•ï¸ DOCTOR PROFILES MODEL
# ============================================

from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base

if TYPE_CHECKING:
    from models.users import User
    # @auto_model
class DoctorProfile(Base):
    __tablename__ = "doctor_profiles"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    qualification = Column(String(100))
    specialization = Column(String(100))
    experience_years = Column(Integer)
    registration_number = Column(String(50))
    clinic_name = Column(String(100))
    clinic_address = Column(String(255))

    user = relationship("User", back_populates="doctor_profile")






