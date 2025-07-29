from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from models.base import Base
from typing import TYPE_CHECKING
from tools.obvious_router import auto_model

if TYPE_CHECKING:
    from models.users import User
    # @auto_model
class UserSetting(Base):
    __tablename__ = "user_settings"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    dark_mode = Column(Boolean, default=False)
    notifications_enabled = Column(Boolean, default=True)

    user = relationship("User", back_populates="user_settings")






