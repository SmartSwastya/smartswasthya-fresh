from typing import TYPE_CHECKING
from models.base import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, JSON, DateTime
from datetime import datetime
from tools.obvious_router import auto_model

# @auto_model
class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id                 = Column(Integer, primary_key=True)
    user_id            = Column(Integer, ForeignKey('users.id'), nullable=False)
    full_name          = Column(String(128), nullable=False)
    date_of_birth      = Column(Date, nullable=True)
    gender             = Column(String(16), nullable=True)
    contact_number     = Column(String(20), nullable=True)
    doctor_name        = Column(String(128), nullable=True)
    recent_appointment = Column(String(128), nullable=True)
    location           = Column(String(256), nullable=True)
    accuracy           = Column(Float(precision=6), nullable=True)
    flat_no            = Column(String(128), nullable=True)
    floor_no           = Column(String(64), nullable=True)
    wing_no            = Column(String(64), nullable=True)
    house_no           = Column(String(128), nullable=True)
    image_url          = Column(String(256), nullable=True)
    preferences        = Column(JSON, nullable=True)
    created_at         = Column(DateTime, default=datetime.utcnow)
    updated_at         = Column(DateTime,
                                default=datetime.utcnow,
                                onupdate=datetime.utcnow)


