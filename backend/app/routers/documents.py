import os
from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.middleware.auth import get_current_user
from app.utils.doc_number import generate_doc_number
from app.services.pdf_service import generate_pdf
from app.services.docx_service import generate_docx

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
    # Ensure output directory exists
    os.makedirs("files", exist_ok=True)

    # Generate document number
    doc_no = generate_doc_number(db)

    # Generate PDF (always)
    pdf_path = f"files/{doc_no}.pdf"
    generate_pdf(db, content, pdf_path)

    # Generate DOCX only for admin
    docx_path = None
    if user["role"] == "admin":
        docx_path = f"files/{doc_no}.docx"
        generate_docx(title, content, docx_path)

    return {
        "document_number": doc_no,
        "pdf": pdf_path,
        "docx": docx_path
    }
