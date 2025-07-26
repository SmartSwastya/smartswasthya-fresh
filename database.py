# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# ========================================================
# 📁 FILE: root/smartswasthya/database.py
# 🧠 Refactored to load DATABASE_URL from .env
# ✅ Includes get_db() for dependency injection
# ========================================================

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from contextlib import contextmanager
from models.base import Base

# 🔄 Load .env values
load_dotenv()

# ✅ Fetch from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment!")

# 🏗 Setup SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 💉 Dependency function for FastAPI routes
@auto_model
@auto_route
@auto_logic
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

