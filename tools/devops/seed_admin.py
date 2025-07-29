from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function

# 🔐 ADMIN SEED SCRIPT — INITIAL SUPERADMIN

import os
from datetime import datetime, timezone
from pathlib import Path
import sys

from alembic_runner import run_migrations
from handler import auto_logic, auto_route, auto_model

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from tools.auth import get_password_hash
from database import SessionLocal
from models.users import User
from models.user_profile_model import UserProfile
from sqlalchemy.orm import Session


@auto_model
@auto_route
@auto_logic
def seed_admin():
    db: Session = SessionLocal()

    admin_list = [
        {
            "full_name": "Admin",
            "email": "smartswasthyaseva@gmail.com",
            "mobile": "9257931868"
        }
    ]

    for admin in admin_list:
        existing = db.query(User).filter(User.email == admin["email"]).first()
        if existing:
            print(f"✅ Admin already exists: {admin['email']}")
            continue

        new_admin = User(
            full_name=admin["full_name"],
            email=admin["email"],
            mobile=admin["mobile"],
            hashed_password=get_password_hash("Dost@1699"),
            is_active=True,
            is_verified=True,
            created_at=datetime.now(timezone.utc)
        )
        db.add(new_admin)
        db.flush()  # ✅ get new_admin.id before commit

        # ⬇️ Add smartuser + admin roles
        profile_roles = ["smartuser", "admin"]
        for role in profile_roles:
            db.add(UserProfile(
                user_id=new_admin.id,
                role=role,
                verified=True
            ))

        print(f"🎉 Admin seeded with roles: {profile_roles} → {admin['email']}")

    db.commit()
    db.close()

if __name__ == "__main__":
    seed_admin()
