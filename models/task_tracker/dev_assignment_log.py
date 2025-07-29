from typing import TYPE_CHECKING
from tools.obvious_router import auto_model
# âœ… models/task_tracker/dev_assignment_log.py

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from models.base import Base

# @auto_model
class DevAssignmentLog(Base):
    __tablename__ = "dev_assignment_log"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, ForeignKey("task_master.task_id"), nullable=False)
    assigned_to = Column(String)  # dev email or ID
    assigned_by = Column(String)
    status = Column(String)  # Assigned / In Progress / Submitted / Reviewed
    remarks = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


