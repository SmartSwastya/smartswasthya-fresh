from typing import TYPE_CHECKING
from models.base import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from tools.obvious_router import auto_model


# @auto_model
class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("inventory_items.id"))
    quantity = Column(Integer)
    transaction_type = Column(String(20))  # issue, return, purchase
    performed_by = Column(String(100))  # staff or vendor name
    timestamp = Column(DateTime)


