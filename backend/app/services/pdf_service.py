import fitz
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from sqlalchemy.orm import Session
from app.models.letterhead import Letterhead

def generate_pdf(db: Session, text: str, output: str):
    lh = db.query(Letterhead).filter(Letterhead.active == True).first()
    if not lh:
        raise RuntimeError("No active letterhead uploaded")

    path = f"app/assets/letterhead/{lh.filename}"

    if lh.filetype == "pdf":
        base = fitz.open(path)
        page = base[0]
        rect = page.rect

        temp = "overlay.pdf"
        c = canvas.Canvas(temp, pagesize=(rect.width, rect.height))
        c.drawString(50, rect.height - 200, text)
        c.save()

        overlay = fitz.open(temp)
        page.show_pdf_page(rect, overlay, 0)
        base.save(output)

    else:
        c = canvas.Canvas(output, pagesize=A4)
        c.drawImage(path, 0, 0, width=A4[0], height=A4[1])
        c.drawString(50, A4[1] - 200, text)
        c.save()
