from typing import TYPE_CHECKING
from tools.obvious_router import auto_model
# âœ… models/task_tracker/code_snippet_map.py
from sqlalchemy.sql import func

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from models.base import Base

# @auto_model
class CodeSnippetMap(Base):
    __tablename__ = "code_snippet_map"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, ForeignKey("task_master.task_id"), nullable=False)
    function_name = Column(String, nullable=True)
    class_name = Column(String, nullable=True)
    snippet_start_line = Column(Integer, nullable=True)
    snippet_end_line = Column(Integer, nullable=True)
    code_excerpt = Column(Text)
    file_path = Column(Text)
    source_version = Column(String)  # v1 or v3


