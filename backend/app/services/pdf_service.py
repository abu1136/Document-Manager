import fitz, os
from reportlab.pdfgen import canvas

def generate_pdf(letterhead, text, out):
    base = fitz.open(letterhead)
    page = base[0]
    rect = page.rect

    temp = "overlay.pdf"
    c = canvas.Canvas(temp, pagesize=(rect.width, rect.height))
    c.drawString(50, rect.height-200, text)
    c.save()

    overlay = fitz.open(temp)
    page.show_pdf_page(rect, overlay, 0)
    base.save(out)
    os.remove(temp)
