# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
# 📁 FILE: logic/family_logic.py
# 📌 PURPOSE: Business logic for Family Dashboard

from sqlalchemy.orm import Session
from models.family_health_status import FamilyHealthStatus
from models.emergency_contacts import EmergencyContact
from database import get_db

# 🔍 Get family health records for user
def get_family_health_status(db: Session, user_id: int):
    return db.query(FamilyHealthStatus).filter(FamilyHealthStatus.user_id == user_id).all()

# 📞 Get emergency contacts for user
def get_emergency_contacts(db: Session, user_id: int):
    return db.query(EmergencyContact).filter(EmergencyContact.user_id == user_id).all()
