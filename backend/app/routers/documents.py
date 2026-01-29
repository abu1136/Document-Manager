from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.document import Document
from app.models.user import User
from app.routers.auth import get_current_user

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("/history")
def document_history(
    doc_no: str | None = Query(None),
    created_by: str | None = Query(None),
    date_from: str | None = Query(None),
    date_to: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Document)

    # 🔐 User restriction
    if current_user.role != "admin":
        query = query.filter(Document.created_by == current_user.id)

    # 🔍 Filters
    if doc_no:
        query = query.filter(Document.document_number.like(f"%{doc_no}%"))

    if created_by and current_user.role == "admin":
        query = query.join(User).filter(User.username.like(f"%{created_by}%"))

    if date_from:
        query = query.filter(Document.created_at >= datetime.fromisoformat(date_from))

    if date_to:
        query = query.filter(Document.created_at <= datetime.fromisoformat(date_to))

    docs = query.order_by(Document.created_at.desc()).all()

    return [
        {
            "document_number": d.document_number,
            "title": d.title,
            "created_by": d.creator.username if d.creator else "Unknown",
            "created_at": d.created_at,
            "pdf_url": f"/files/{d.pdf_path}" if d.pdf_path else None,
        }
        for d in docs
    ]
