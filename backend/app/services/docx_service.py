from docx import Document

def generate_docx(title, content, out):
    d = Document()
    d.add_heading(title, 1)
    d.add_paragraph(content)
    d.save(out)
