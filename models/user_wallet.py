from tools.obvious_router import auto_model
#region auto_model
# ============================================
from sqlalchemy.sql import func
# ðŸ’° USER WALLET MODEL # ðŸ”˜ Patch test line by ChatGPT # ðŸ”˜ Patch test line by ChatGPT
# ============================================

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.users import User
    # @auto_model
class UserWallet(Base):
    __tablename__ = "user_wallet"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    balance = Column(Float)

    user = relationship("User", back_populates="wallet")






