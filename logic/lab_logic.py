# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
# 📁 FILE: logic/lab_logic.py
# 📌 PURPOSE: Business logic for Lab Dashboard

from sqlalchemy.orm import Session
from models.lab_profiles import LabProfile
from models.lab_test_results import LabTestResult
from database import get_db

# 🔍 Fetch lab profile for current user
def get_lab_profile_by_user(db: Session, user_id: int):
    return db.query(LabProfile).filter(LabProfile.user_id == user_id).first()

# 📄 Get recent test results (example: last 10)
def get_recent_lab_tests(db: Session, lab_id: int):
    return (
        db.query(LabTestResult)
        .filter(LabTestResult.lab_id == lab_id)
        .order_by(LabTestResult.test_date.desc())
        .limit(10)
        .all()
    )
