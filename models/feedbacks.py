from models.base import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING
from tools.obvious_router import auto_model

if TYPE_CHECKING:
    from models.users import User
    # @auto_model
class Feedback(Base):
    __tablename__ = "feedbacks"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    service_type = Column(String(50))  # doctor, lab, ambulance, etc.
    service_id = Column(Integer)
    rating = Column(Integer)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime)

    user = relationship("User", back_populates="feedbacks")






