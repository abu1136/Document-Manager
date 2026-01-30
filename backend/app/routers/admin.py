from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import os
import shutil

from app.database import get_db
from app.models.user import User
from app.models.letterhead import Letterhead
from app.routers.auth import get_current_user
from app.utils.security import hash_password

router = APIRouter(prefix="/admin", tags=["Admin"])


# ===============================
# CREATE USER
# ===============================
@router.post("/create-user")
def create_user(
    username: str,
    password: str,
    role: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(
        username=username,
        password=hash_password(password),
        role=role
    )
    db.add(user)
    db.commit()

    return {"message": "User created successfully"}


# ===============================
# LIST USERS
# ===============================
@router.get("/users")
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    users = db.query(User).all()
    return [
        {"id": u.id, "username": u.username, "role": u.role}
        for u in users
    ]


# ===============================
# RESET USER PASSWORD (STEP E – PART 2)
# ===============================
@router.post("/reset-password")
def reset_user_password(
    user_id: int,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = hash_password(new_password)
    db.commit()

    return {"message": f"Password reset for user '{user.username}'"}


# ===============================
# UPLOAD LETTERHEAD
# ===============================
@router.post("/letterhead")
def upload_letterhead(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    upload_dir = "files/letterhead"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # deactivate old letterheads
    db.query(Letterhead).update({"active": False})

    letterhead = Letterhead(
        file_path=file_path,
        active=True
    )
    db.add(letterhead)
    db.commit()

    return {"message": "Letterhead uploaded successfully"}
