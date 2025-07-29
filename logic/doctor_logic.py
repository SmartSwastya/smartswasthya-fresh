# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
# 📁 FILE: logic/doctor_logic.py
# 📌 PURPOSE: Business logic for Doctor Dashboard

from sqlalchemy.orm import Session
from models.doctor_profiles import DoctorProfile
from database import get_db

# 🔍 Fetch all doctor profiles (for admin/staff view)
def get_all_doctors(db: Session):
    return db.query(DoctorProfile).all()

# 🔍 Fetch specific doctor profile (for logged-in user)
def get_doctor_profile_by_user(db: Session, user_id: int):
    return db.query(DoctorProfile).filter(DoctorProfile.user_id == user_id).first()

# 🔄 Placeholder for metrics / analytics
def get_doctor_metrics(user_id: int):
    # Future: Fetch doctor-wise appointments, feedback, ratings etc.
    return {
        "total_appointments": 0,
        "active_patients": 0,
        "avg_feedback_score": None
    }
