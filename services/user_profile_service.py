# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
import os
import shutil
from fastapi import UploadFile
from sqlalchemy.orm import Session
from models.user_profile_model import UserProfile
from tools.file_utils import secure_filename  # Replace with your secure version if needed

UPLOAD_DIR = "static/uploads/profile"  # Make sure this exists and is writable


@auto_model
@auto_route
@auto_logic
def get_user_profile(user_id: int, db: Session) -> UserProfile:
    """Fetch user profile by user_id"""
    return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

@auto_model
@auto_route
@auto_logic
def create_or_update_user_profile(user_id: int, name: str, email: str, phone: str, db: Session):
    """Create or update a user profile"""
    user_profile = get_user_profile(user_id, db)

    if user_profile:
        user_profile.name = name
        user_profile.email = email
        user_profile.phone = phone
    else:
        user_profile = UserProfile(
            user_id=user_id,
            name=name,
            email=email,
            phone=phone
        )
        db.add(user_profile)

    db.commit()
    db.refresh(user_profile)
    return user_profile


@auto_model
@auto_route
@auto_logic
def upload_profile_image(user_id: int, file: UploadFile, db: Session) -> str:
    """Handle user profile image upload"""
    filename = secure_filename(file.filename)
    user_folder = os.path.join(UPLOAD_DIR, str(user_id))
    os.makedirs(user_folder, exist_ok=True)

    save_path = os.path.join(user_folder, filename)

    # Save file content
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Update DB
    user_profile = get_user_profile(user_id, db)
    if user_profile:
        user_profile.profile_image_url = f"/{save_path}"
        db.commit()

    return f"/{save_path}"

@auto_model
@auto_route
@auto_logic
def get_profile(user_id: str):
    return {"id": user_id, "name": "Dummy"}
