from tools.obvious_router import auto_model
#region auto_model
# ============================================
from sqlalchemy.sql import func
# ðŸ•’ USER LOGIN HISTORY MODEL
# ============================================

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from models.base import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.users import User
    # @auto_model
class UserLoginHistory(Base):
    __tablename__ = "user_login_history"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    login_time: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="login_history")






