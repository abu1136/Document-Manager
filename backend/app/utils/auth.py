from passlib.context import CryptContext
from jose import jwt
import os, datetime

pwd = CryptContext(schemes=["bcrypt"])
SECRET = os.getenv("JWT_SECRET")

def hash_pass(p): return pwd.hash(p)
def verify(p,h): return pwd.verify(p,h)

def create_token(data):
    data["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    return jwt.encode(data, SECRET, algorithm="HS256")
