import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.middleware.auth import get_current_user
from app.models.letterhead import Letterhead

UPLOAD_DIR = "app/assets/letterhead"

router = APIRouter(prefix="/admin", tags=["admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/letterhead")
def upload_letterhead(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    ext = file.filename.split(".")[-1].lower()
    if ext not in ["pdf", "png", "jpg", "jpeg"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    filetype = "pdf" if ext == "pdf" else "image"

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    filename = f"letterhead.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Deactivate old letterheads
    db.query(Letterhead).update({"active": False})

    lh = Letterhead(
        filename=filename,
        filetype=filetype,
        uploaded_by=user["user_id"],
        active=True
    )

    db.add(lh)
    db.commit()

    return {
        "status": "success",
        "filename": filename,
        "type": filetype
    }
