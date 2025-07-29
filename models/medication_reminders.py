from models.base import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING
from tools.obvious_router import auto_model

if TYPE_CHECKING:
    from models.users import User
    # @auto_model
class MedicationReminder(Base):
    __tablename__ = "medication_reminders"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    medicine_name = Column(String(100))
    dosage = Column(String(50))
    reminder_time = Column(DateTime)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="medication_reminders")






