import fitz  # PyMuPDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import tempfile
import os


def generate_pdf(
    letterhead_path: str,
    content: str,
    document_id: str,
    output_path: str
):
    """
    Generate a PDF using a letterhead PDF/image as background
    and overlay the document content text + footer with document ID.
    """

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Temporary content PDF
    fd, temp_pdf = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)

    c = canvas.Canvas(temp_pdf, pagesize=A4)
    width, height = A4

    # -------- Main content --------
    text = c.beginText(25 * mm, height - 40 * mm)
    text.setFont("Helvetica", 11)

    for line in content.splitlines():
        text.textLine(line)

    c.drawText(text)

    # -------- Footer (Document Identifier) --------
    c.setFont("Helvetica", 8)
    footer_text = f"Document ID: {document_id}"
    c.drawRightString(
        width - 20 * mm,
        15 * mm,
        footer_text
    )

    c.showPage()
    c.save()

    # -------- Merge with letterhead --------
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
