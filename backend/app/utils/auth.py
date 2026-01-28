from passlib.context import CryptContext
from jose import jwt
import os
import datetime

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET = os.getenv("JWT_SECRET", "changeme")


def _bcrypt_safe(password: str) -> str:
    """
    Ensure password is safe for bcrypt (max 72 bytes).
    Truncate AFTER utf-8 encoding, then decode back to str.
    """
    pwd_bytes = password.encode("utf-8")
    safe_bytes = pwd_bytes[:72]
    return safe_bytes.decode("utf-8", errors="ignore")


def hash_pass(password: str) -> str:
    return pwd_context.hash(_bcrypt_safe(password))


def verify(password: str, password_hash: str) -> bool:
    return pwd_context.verify(
        _bcrypt_safe(password),
        password_hash
    )


def create_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    return jwt.encode(payload, SECRET, algorithm="HS256")
