from passlib.context import CryptContext
from jose import jwt
import os
import datetime

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

SECRET = os.getenv("JWT_SECRET", "changeme")


def hash_pass(password: str) -> str:
    return pwd_context.hash(password)


def verify(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    return jwt.encode(payload, SECRET, algorithm="HS256")
