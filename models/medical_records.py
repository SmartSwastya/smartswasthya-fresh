from typing import TYPE_CHECKING
from typing import TYPE_CHECKING
from tools.obvious_router import auto_model
#region auto_model
# ============================================
from sqlalchemy.sql import func
# ðŸ—‚ï¸ MEDICAL RECORDS MODEL
# ============================================

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime

# @auto_model
class MedicalRecord(Base):
    __tablename__ = "medical_records"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    record_type = Column(String)
    description = Column(String)
    date = Column(DateTime)

    user = relationship("User", back_populates="medical_records")




if TYPE_CHECKING:
    from models.users import User
    
