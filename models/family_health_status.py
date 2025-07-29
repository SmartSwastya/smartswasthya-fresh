from typing import TYPE_CHECKING
from typing import TYPE_CHECKING
from tools.obvious_router import auto_model
#region auto_model
# ============================================
from sqlalchemy.sql import func
# ðŸ‘¨â€ðŸ‘©â€ðŸ‘§ FAMILY HEALTH STATUS MODEL
# ============================================

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base

# @auto_model
class FamilyHealthStatus(Base):
    __tablename__ = "family_health_status"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    condition = Column(String)
    relation = Column(String)

    user = relationship("User", back_populates="family_health_status")




if TYPE_CHECKING:
    from models.users import User
    
