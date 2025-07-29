from models.base import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING
from tools.obvious_router import auto_model

if TYPE_CHECKING:
    from models.users import User
    # @auto_model
class OrderServiceTracking(Base):
    __tablename__ = "order_service_tracking"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    order_id = Column(String(100))
    service_status = Column(String(100))  # e.g., "pending", "dispatched", "delivered"
    updated_at = Column(DateTime)

    user = relationship("User", back_populates="order_service_tracking")






