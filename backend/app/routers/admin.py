import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import SessionLocal
from app.middleware.auth import get_current_user
from app.models.user import User
from app.models.letterhead import Letterhead
from app.utils.auth import hash_pass

UPLOAD_DIR = "app/assets/letterhead"

router = APIRouter(prefix="/admin", tags=["admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_admin(user):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")


# ===================== USERS =====================

@router.get("/users")
def list_users(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    require_admin(user)
    users = db.query(User).all()
    return [
        {"id": u.id, "username": u.username, "role": u.role}
        for u in users
    ]


@router.post("/users")
def create_user(
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    require_admin(user)

    if role not in ("admin", "user"):
        raise HTTPException(status_code=400, detail="Invalid role")

    try:
        new_user = User(
            username=username,
            password_hash=hash_pass(password),
            role=role
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")

    return {"status": "user_created"}


# ===================== LETTERHEAD =====================

@router.post("/letterhead")
def upload_letterhead(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    require_admin(user)

    ext = file.filename.split(".")[-1].lower()
    if ext not in ("pdf", "png", "jpg", "jpeg"):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    filename = f"letterhead.{ext}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db.query(Letterhead).update({"active": False})

    lh = Letterhead(
        filename=filename,
        filetype="pdf" if ext == "pdf" else "image",
        uploaded_by=user["user_id"],
        active=True
    )

    db.add(lh)
    db.commit()

    return {"status": "letterhead_uploaded"}
