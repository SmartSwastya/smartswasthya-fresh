from typing import TYPE_CHECKING
from tools.obvious_router import auto_model
# âœ… models/task_tracker/model_trace.py
from sqlalchemy.sql import func

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from models.base import Base

# @auto_model
class ModelTrace(Base):
    __tablename__ = "model_trace"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, ForeignKey("task_master.task_id"), nullable=False)
    model_name = Column(String, nullable=False)
    model_file_path = Column(String, nullable=True)
    found = Column(Boolean, default=False)  # True = Found, False = Missing


