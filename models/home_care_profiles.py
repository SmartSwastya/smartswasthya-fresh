from __future__ import annotations
from tools.obvious_router import auto_model
#region auto_model
# ============================================
from sqlalchemy.sql import func
# ðŸ¡ HOME CARE PROFILES MODEL
# ============================================

from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base

if TYPE_CHECKING:
    from models.users import User
    # @auto_model
class HomeCareProfile(Base):
    __tablename__ = "home_care_profiles"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    provider_name = Column(String(100))
    contact_number = Column(String(20))
    services_offered = Column(String(255))
    address = Column(String(255))

    user = relationship("User", back_populates="home_care_profile")






