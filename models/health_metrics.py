from tools.obvious_router import auto_model
#region auto_model
# ============================================
from sqlalchemy.sql import func
# â¤ï¸â€ðŸ©¹ HEALTH METRICS MODEL
# ============================================

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.users import User
    # @auto_model
class HealthMetric(Base):
    __tablename__ = "health_metrics"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    metric_type = Column(String)
    value = Column(Float)

    user = relationship("User", back_populates="health_metrics")






