from typing import TYPE_CHECKING
from models.base import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime
from tools.obvious_router import auto_model


# @auto_model
class ServicePackage(Base):
    __tablename__ = "service_packages"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text)
    price = Column(Float)
    is_active = Column(Boolean, default=True)


