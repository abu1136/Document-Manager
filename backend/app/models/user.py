from sqlalchemy import Column, Integer, String, Enum
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password_hash = Column(String(255))
    role = Column(Enum("admin","user"))
