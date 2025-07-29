from typing import TYPE_CHECKING
from models.base import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime
from tools.obvious_router import auto_model


# @auto_model
#region auto_model
class StaffProfile(Base):
    __tablename__ = "staff_profiles"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    role = Column(String(50))  # e.g., nurse, technician, attendant
    contact_number = Column(String(20))
    joined_at = Column(DateTime)


