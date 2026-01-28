from passlib.context import CryptContext
from jose import jwt
import os
import datetime

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET = os.getenv("JWT_SECRET", "changeme")


def _normalize_password(password: str) -> bytes:
    """
    bcrypt supports max 72 bytes.
    Truncate safely after UTF-8 encoding.
    """
    return password.encode("utf-8")[:72]


def hash_pass(password: str) -> str:
    return pwd_context.hash(_normalize_password(password))


def verify(password: str, password_hash: str) -> bool:
    return pwd_context.verify(
        _normalize_password(password),
        password_hash
    )


def create_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    return jwt.encode(payload, SECRET, algorithm="HS256")
