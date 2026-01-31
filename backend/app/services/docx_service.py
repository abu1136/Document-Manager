from docx import Document

def generate_docx(content, output_path, document_id, title):
    """
    Generate a DOCX file with the given content
    """
    d = Document()
    d.add_heading(title, 1)
    d.add_paragraph(content)
    d.add_paragraph("")
    d.add_paragraph(f"Document ID: {document_id}", style='Caption')
    d.save(output_path)
