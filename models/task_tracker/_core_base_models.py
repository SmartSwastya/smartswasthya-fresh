from typing import TYPE_CHECKING
# models/task_tracker/_core_base_models.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from models.base import Base
from tools.obvious_router import auto_model

@auto_model
class TaskMaster(Base):
    __tablename__ = "task_master"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, nullable=False)
    title = Column(Text)
    description = Column(Text)
    source = Column(String)
    source_layer = Column(String)
    matched_file = Column(String)
    matched_file_paths = Column(Text)
    matched_file_count = Column(Integer)
    model_name = Column(String)
    model_file = Column(String)
    auto_status = Column(String)
    reason = Column(Text)
    ref_snippet = Column(Text)

def get_model():
    return TaskMaster