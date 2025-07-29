from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String
from models.base import Base  # âœ… for FastAPI/SQLAlchemy declarative base
from tools.obvious_router import auto_model

# @auto_model
class LegacyUser(Base):
    __tablename__ = 'legacy_users'
    id = Column(Integer, primary_key=True)
    role = Column(String(50))
    name = Column(String(100))
    mobile = Column(String(15), unique=True, nullable=False)
    email = Column(String(100))


