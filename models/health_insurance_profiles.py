from models.base import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING
from tools.obvious_router import auto_model

if TYPE_CHECKING:
    from models.users import User
    # @auto_model
class HealthInsuranceProfile(Base):
    __tablename__ = "health_insurance_profiles"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    insurer_name = Column(String(100))
    policy_number = Column(String(100))
    coverage_details = Column(Text)
    valid_till = Column(DateTime)

    user = relationship("User", back_populates="health_insurance_profiles")






