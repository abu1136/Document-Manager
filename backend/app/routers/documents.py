import os
from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.middleware.auth import get_current_user
from app.models.letterhead import Letterhead
from app.models.document import Document
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
    letterhead = db.query(Letterhead).filter(Letterhead.active == True).first()
    if not letterhead:
        raise HTTPException(status_code=400, detail="No active letterhead")

    doc_no = generate_doc_number(db)

    pdf_path = f"files/{doc_no}.pdf"
    generate_pdf(
        letterhead_path=f"app/assets/letterhead/{letterhead.filename}",
        content=content,
        output_path=pdf_path,
        document_id=doc_no
    )

    docx_path = None
    if user["role"] == "admin":
        docx_path = f"files/{doc_no}.docx"
        generate_docx(title, content, docx_path)

    # ✅ Save document history
    doc = Document(
        document_number=doc_no,
        title=title,
        pdf_path=pdf_path,
        docx_path=docx_path,
        created_by=user["user_id"]
    )

    db.add(doc)
    db.commit()

    return {
        "document_number": doc_no,
        "pdf": pdf_path,
        "docx": docx_path
    }


@router.get("/history")
def document_history(
    q: str = "",
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Document)

    if user["role"] != "admin":
        query = query.filter(Document.created_by == user["user_id"])

    if q:
        query = query.filter(Document.document_number.contains(q))

    return query.order_by(Document.created_at.desc()).all()
