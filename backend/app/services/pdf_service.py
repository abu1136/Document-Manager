import fitz  # PyMuPDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import tempfile
import os


def generate_pdf(letterhead_path: str, content: str, output_path: str):
    """
    Generate a PDF using a letterhead PDF/image as background
    and overlay the document content text.
    """

    # Create a temporary PDF with the content text
    fd, temp_pdf = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)

    c = canvas.Canvas(temp_pdf, pagesize=A4)
    width, height = A4

    text = c.beginText(50, height - 150)
    for line in content.splitlines():
        text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()

    # Merge letterhead + content
    base = fitz.open(letterhead_path)
    overlay = fitz.open(temp_pdf)

    base_page = base[0]
    base_page.show_pdf_page(
        base_page.rect,
        overlay,
        0
    )

    base.save(output_path)
    base.close()
    overlay.close()

    os.remove(temp_pdf)
