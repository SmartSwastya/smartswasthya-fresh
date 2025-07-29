from tools.obvious_router import auto_model
#region auto_model
# ============================================
from sqlalchemy.sql import func
# ðŸ”— REFERRAL LINKS MODEL
# ============================================

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.users import User
    from models.referral_earnings import ReferralEarning
    # @auto_model
class ReferralLink(Base):
    __tablename__ = "referral_links"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    referral_code = Column(String(50), unique=True, index=True)
    created_at = Column(DateTime)

    user = relationship("User", back_populates="referral_links")
    earnings = relationship("models.referral_earnings.ReferralEarning", back_populates="referral_link")






