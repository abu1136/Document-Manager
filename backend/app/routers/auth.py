from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.utils.auth import hash_pass, verify, create_token

router = APIRouter(prefix="/auth", tags=["auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/setup/status")
def setup_status(db: Session = Depends(get_db)):
    admin_exists = db.query(User).filter(User.role == "admin").count() > 0
    return {"setup_required": not admin_exists}


@router.post("/setup")
def setup_admin(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Check if admin already exists
    if db.query(User).filter(User.role == "admin").count() > 0:
        raise HTTPException(status_code=403, detail="Admin already configured")

    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")

    admin = User(
        username=username,
        password_hash=hash_pass(password),
        role="admin"
    )

    db.add(admin)
    db.commit()

    return {"status": "admin_created"}


@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({
        "user_id": user.id,
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
