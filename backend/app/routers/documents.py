import os
from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.middleware.auth import get_current_user
from app.models.letterhead import Letterhead
from app.services.pdf_service import generate_pdf
from app.services.docx_service import generate_docx
from app.utils.doc_number import generate_doc_number

router = APIRouter(prefix="/documents", tags=["documents"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("")
def create_document(
    title: str = Form(...),
    content: str = Form(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Active letterhead check
    letterhead = (
        db.query(Letterhead)
        .filter(Letterhead.active == True)
        .first()
    )

    if not letterhead:
        raise HTTPException(
            status_code=400,
            detail="No active letterhead configured. Contact admin."
        )

    letterhead_path = os.path.join(
        "app/assets/letterhead",
        letterhead.filename
    )

    if not os.path.exists(letterhead_path):
        raise HTTPException(
            status_code=500,
            detail="Letterhead file missing on server"
        )

    os.makedirs("files", exist_ok=True)

    doc_no = generate_doc_number(db)

    pdf_path = f"files/{doc_no}.pdf"

    # ✅ PASS document identifier to PDF service
    generate_pdf(
        letterhead_path=letterhead_path,
        content=content,
        output_path=pdf_path,
        document_id=doc_no
    )

    docx_path = None
    if user["role"] == "admin":
        docx_path = f"files/{doc_no}.docx"
        generate_docx(title, content, docx_path)

    return {
        "document_number": doc_no,
        "pdf": pdf_path,
        "docx": docx_path
    }
