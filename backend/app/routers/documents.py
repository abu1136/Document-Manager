from fastapi import APIRouter, Depends, Query, Form, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import os
import re

from app.database import get_db
from app.models.document import Document
from app.models.user import User
from app.models.letterhead import Letterhead
from app.routers.auth import get_current_user
from app.utils.doc_number import generate_doc_number
from app.services.pdf_service import generate_pdf
from app.services.docx_service import generate_docx

router = APIRouter()


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent directory traversal and injection attacks"""
    # Remove path separators and special characters
    filename = os.path.basename(filename)
    # Remove any characters that aren't alphanumeric, dot, dash, or underscore
    filename = re.sub(r'[^\w\-.]', '_', filename)
    return filename


@router.post("/create")
def create_document(
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new document with PDF and DOCX generation"""
    
    # Generate document number
    doc_number = generate_doc_number(db)
    
    # Get active letterhead
    letterhead = db.query(Letterhead).filter(Letterhead.active.is_(True)).first()
    if not letterhead:
        raise HTTPException(status_code=400, detail="No active letterhead found. Please upload a letterhead first.")
    
    # Create sanitized filenames
    safe_doc_id = doc_number.replace('/', '_')
    pdf_filename = f"{safe_doc_id}.pdf"
    docx_filename = f"{safe_doc_id}.docx"
    pdf_path = os.path.join("documents", pdf_filename)
    docx_path = os.path.join("documents", docx_filename)
    
    # Ensure directories exist
    os.makedirs("files/documents", exist_ok=True)
    
    # Full paths for file operations
    full_pdf_path = os.path.join("files", pdf_path)
    full_docx_path = os.path.join("files", docx_path)
    
    # Sanitize letterhead filename and construct path
    safe_letterhead_filename = sanitize_filename(letterhead.filename)
    letterhead_path = os.path.join("files/letterhead", safe_letterhead_filename)
    
    # Generate documents with standardized parameter order
    try:
        generate_pdf(letterhead_path, content, doc_number, full_pdf_path)
        generate_docx(title, content, doc_number, full_docx_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating documents: {str(e)}")
    
    # Save to database
    document = Document(
        document_number=doc_number,
        title=title,
        pdf_path=pdf_path,
        docx_path=docx_path,
        created_by=current_user.id
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return {
        "message": "Document created successfully",
        "document_number": doc_number,
        "pdf_url": f"/files/{pdf_path}",
        "docx_url": f"/files/{docx_path}"
    }


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
