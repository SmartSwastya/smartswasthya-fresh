from typing import TYPE_CHECKING
from tools.obvious_router import auto_model
# âœ… models/task_tracker/task_status_history.py

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from models.base import Base

# @auto_model
class TaskStatusHistory(Base):
    __tablename__ = "task_status_history"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, ForeignKey("task_master.task_id"), nullable=False)
    status = Column(String)  # e.g., âœ…, ðŸ§ , âŒ, etc.
    changed_by = Column(String)  # e.g., admin ID or system
    reason = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


