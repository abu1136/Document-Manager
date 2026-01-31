from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.routers.auth import get_current_user
from app.utils.security import verify_password, hash_password

router = APIRouter()


@router.post("/change-password")
def change_password(
    current_password: str = Form(...),
    new_password: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not verify_password(current_password, current_user.password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    current_user.password = hash_password(new_password)
    db.commit()

    return {"message": "Password updated successfully"}
