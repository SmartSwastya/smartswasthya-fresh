from typing import TYPE_CHECKING
from typing import TYPE_CHECKING
from tools.obvious_router import auto_model
#region auto_model
# ============================================
from sqlalchemy.sql import func
# ðŸ§¾ PRESCRIPTIONS MODEL
# ============================================

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime

# @auto_model
class Prescription(Base):
    __tablename__ = "prescriptions"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    medicine = Column(String)
    dosage = Column(String)
    prescribed_on = Column(DateTime)

    user = relationship("User", back_populates="prescriptions")




if TYPE_CHECKING:
    from models.users import User
    
