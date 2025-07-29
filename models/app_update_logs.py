from typing import TYPE_CHECKING
from models.base import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime
from tools.obvious_router import auto_model


# @auto_model
class AppUpdateLog(Base):
    __tablename__ = "app_update_logs"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    version = Column(String(20))
    platform = Column(String(20))  # android, ios
    description = Column(String(255))
    released_at = Column(DateTime)


