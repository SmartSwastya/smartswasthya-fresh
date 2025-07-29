from __future__ import annotations
from tools.obvious_router import auto_model
#region auto_model
# ============================================
from sqlalchemy.sql import func
# ðŸ‘¨â€âš•ï¸ PHARMACY PROFILES MODEL
# ============================================

from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base

if TYPE_CHECKING:
    from models.users import User
    # @auto_model
class PharmacyProfile(Base):
    __tablename__ = "pharmacy_profiles"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    license_number = Column(String(100))
    pharmacy_name = Column(String(100))
    owner_name = Column(String(100))
    contact_number = Column(String(20))
    address = Column(String(255))

    user = relationship("User", back_populates="pharmacy_profile")






