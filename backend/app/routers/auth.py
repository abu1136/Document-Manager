from fastapi import APIRouter, Depends, HTTPException, Header, Form
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from app.database import get_db
from app.models import User

SECRET_KEY = "CHANGE_ME"
ALGORITHM = "HS256"
TOKEN_EXPIRY_HOURS = 8

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    token = authorization.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({
        "sub": user.id,
        "role": user.role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRY_HOURS)
    }, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "role": user.role, "username": user.username}


@router.get("/setup/status")
def setup_status(db: Session = Depends(get_db)):
    """Check if initial admin setup is required"""
    admin_exists = db.query(User).filter(User.role == "admin").first()
    return {"setup_required": admin_exists is None}


@router.post("/setup")
def setup_admin(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """Create the initial admin user"""
    # Check if admin already exists
    if db.query(User).filter(User.role == "admin").first():
        raise HTTPException(status_code=400, detail="Admin already exists")
    
    # Create admin user
    admin = User(
        username=username,
        password=get_password_hash(password),
        role="admin"
    )
    db.add(admin)
    db.commit()
    
    return {"message": "Admin created successfully"}
