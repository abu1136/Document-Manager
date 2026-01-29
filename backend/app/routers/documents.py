from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.document import Document
from app.models.user import User
from app.routers.auth import get_current_user

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("/history")
def document_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Document)

    # User → only own documents
    if current_user.role != "admin":
        query = query.filter(Document.created_by == current_user.id)

    docs = query.order_by(Document.created_at.desc()).all()

    return [
        {
            "id": d.id,
            "document_number": d.document_number,
            "title": d.title,
            "created_at": d.created_at,
            "created_by": d.creator.username if d.creator else "Unknown",
            "pdf_url": f"/files/{d.pdf_path}" if d.pdf_path else None
        }
        for d in docs
    ]
