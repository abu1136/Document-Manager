from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.middleware.auth import get_current_user
from app.models.user import User
from app.utils.auth import verify, hash_pass

router = APIRouter(prefix="/profile", tags=["profile"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/change-password")
def change_password(
    old_password: str = Form(...),
    new_password: str = Form(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    u = db.query(User).filter(User.id == user["user_id"]).first()

    if not verify(old_password, u.password_hash):
        raise HTTPException(status_code=400, detail="Old password incorrect")

    u.password_hash = hash_pass(new_password)
    db.commit()

    return {"status": "password_updated"}
