from models.base import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING
from tools.obvious_router import auto_model

if TYPE_CHECKING:
    from models.users import User
    # @auto_model
class BillingInvoice(Base):
    __tablename__ = "billing_invoices"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    invoice_number = Column(String(50), unique=True)
    amount = Column(Float)
    issued_at = Column(DateTime)
    status = Column(String(20))  # paid, unpaid, cancelled

    user = relationship("User", back_populates="billing_invoices")






