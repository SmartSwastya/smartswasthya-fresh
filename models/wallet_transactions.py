from typing import TYPE_CHECKING
from typing import TYPE_CHECKING
from tools.obvious_router import auto_model
#region auto_model
# ============================================
from sqlalchemy.sql import func
# ðŸ’¸ WALLET TRANSACTIONS MODEL
# ============================================

# models/wallet_transactions.py
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime

# @auto_model
class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="wallet_transactions")




if TYPE_CHECKING:
    from models.users import User
    
