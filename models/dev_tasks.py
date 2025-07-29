from typing import TYPE_CHECKING
from tools.obvious_router import auto_model
# File: models/dev_tasks.py

from sqlalchemy import Column, Integer, String, Text, Enum, Float, DateTime
from sqlalchemy.sql import func
from models.base import Base
import enum

class TaskStatusEnum(str, enum.Enum):
    new = "new"
    assigned = "assigned"
    in_progress = "in_progress"
    submitted = "submitted"
    reviewing = "reviewing"
    rejected = "rejected"
    done = "done"
    partial = "partial"
    duplicate = "duplicate"
    not_required = "not_required"

# @auto_model
class DevTask(Base):
    __tablename__ = "dev_tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(32), unique=True, nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    source_file = Column(String(255))
    mapped_file = Column(String(255))
    logic_score = Column(Float)
    status = Column(
        Enum(TaskStatusEnum, name="taskstatusenum", native_enum=True, create_type=True),
        default=TaskStatusEnum.new,
        nullable=False
    )
    blueprint_ref = Column(String(255))
    assigned_to = Column(String(100))
    admin_remarks = Column(Text)
    module_group = Column(String(100))  # âœ… NEW FIELD ADDED
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


