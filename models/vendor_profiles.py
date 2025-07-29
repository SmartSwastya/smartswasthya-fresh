from models.base import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING
from tools.obvious_router import auto_model

if TYPE_CHECKING:
    from models.users import User
    # @auto_model
class VendorProfile(Base):
    __tablename__ = "vendor_profiles"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(100))
    service_type = Column(String(50))  # e.g., CCTV, pharmacy supplier
    registered_at = Column(DateTime)
    contact_email = Column(String(100))

    user = relationship("User", back_populates="vendor_profiles")






