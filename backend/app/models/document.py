from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    document_number = Column(String(50), unique=True)
    title = Column(String(255))
    content = Column(Text)
    requested_by = Column(Integer, ForeignKey("users.id"))
    file_pdf = Column(String(255))
    file_docx = Column(String(255))
