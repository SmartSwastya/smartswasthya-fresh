from tools.obvious_router import auto_model
#region auto_model
# ============================================
from sqlalchemy.sql import func
# ðŸ“¦ REFERRAL EARNINGS MODEL
# ============================================

from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.users import User
    from models.referral_links import ReferralLink
    # @auto_model
class ReferralEarning(Base):
    __tablename__ = "referral_earnings"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    referral_link_id = Column(Integer, ForeignKey("referral_links.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    created_at = Column(DateTime)

    referral_link = relationship("models.referral_links.ReferralLink", back_populates="earnings")
    user = relationship("User", back_populates="referral_earnings")






