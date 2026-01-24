from fastapi import FastAPI, Depends, Form
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.utils.doc_number import generate_doc_number
from app.services.pdf_service import generate_pdf
from app.services.docx_service import generate_docx
import os

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/documents")
def create_doc(
    title: str = Form(...),
    content: str = Form(...),
    role: str = Form(...),
    db: Session = Depends(get_db)
):
    doc_no = generate_doc_number(db)

    os.makedirs("files", exist_ok=True)
    pdf_path = f"files/{doc_no}.pdf"

    generate_pdf(
        os.getenv("LETTERHEAD_PATH"),
        content,
        pdf_path
    )

    docx_path = None
    if role == "admin":
        docx_path = f"files/{doc_no}.docx"
        generate_docx(title, content, docx_path)

    return {
        "document_number": doc_no,
        "pdf": pdf_path,
        "docx": docx_path
    }
