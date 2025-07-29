from typing import TYPE_CHECKING
from models.base import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Text, DateTime
from tools.obvious_router import auto_model


# @auto_model
class InventoryItem(Base):
    __tablename__ = "inventory_items"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    category = Column(String(50))
    description = Column(Text)
    added_on = Column(DateTime)


