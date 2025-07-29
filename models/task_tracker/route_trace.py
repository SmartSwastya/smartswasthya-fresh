from typing import TYPE_CHECKING
from tools.obvious_router import auto_model
# âœ… models/task_tracker/route_trace.py
from sqlalchemy.sql import func

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from models.base import Base
from tools.smart_logger import SmartLogger
logger = SmartLogger("RouteTrace")
# @auto_model
class RouteTrace(Base):
    __tablename__ = "route_trace"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, ForeignKey("task_master.task_id"), nullable=False)
    endpoint = Column(String, nullable=True)       # e.g. /user/login
    method = Column(String, nullable=True)         # GET, POST, etc.
    router_function = Column(String, nullable=True)
    file_path = Column(String, nullable=True)


