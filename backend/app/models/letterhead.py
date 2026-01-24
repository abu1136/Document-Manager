from sqlalchemy import Column, Integer, String, Enum, Boolean, ForeignKey
from app.database import Base

class Letterhead(Base):
    __tablename__ = "letterhead"

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    filetype = Column(Enum("pdf", "image"), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    active = Column(Boolean, default=True)
