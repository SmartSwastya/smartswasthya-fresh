from tools.obvious_router import auto_model
#region auto_model
# ============================================
from sqlalchemy.sql import func
# âš¡ ELECTRONIC DEVICES MODEL
# ============================================

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.users import User
    # @auto_model
class ElectronicDevice(Base):
    __tablename__ = "ele_devices"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    device_type = Column(String)
    serial_number = Column(String)

    user = relationship("User", back_populates="ele_devices")






