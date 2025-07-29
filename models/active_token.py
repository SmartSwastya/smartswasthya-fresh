from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, DateTime
from models.base import Base  # ya extensions.db agar use ho raha hai
from tools.obvious_router import auto_model

# @auto_model
class ActiveToken(Base):
    __tablename__ = 'active_tokens'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime)
    expires_at = Column(DateTime)


