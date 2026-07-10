from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, Cookie, status
import os
import hashlib
import base64
from .config import load_app_env

load_app_env()

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


def hash_password(password: str) -> str:
    """Hash password using standard library PBKDF2-HMAC-SHA256 (no external C dependencies)."""
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    salt_b64 = base64.b64encode(salt).decode('utf-8')
    hash_b64 = base64.b64encode(dk).decode('utf-8')
    return f"pbkdf2_sha256$100000${salt_b64}${hash_b64}"


def verify_password(plain: str, hashed: str) -> bool:
    """Verify password by checking PBKDF2-HMAC-SHA256 or falling back to bcrypt."""
    if hashed.startswith("pbkdf2_sha256$"):
        try:
            parts = hashed.split("$")
            if len(parts) != 4:
                return False
            iterations = int(parts[1])
            salt = base64.b64decode(parts[2])
            stored_hash = base64.b64decode(parts[3])
            dk = hashlib.pbkdf2_hmac('sha256', plain.encode('utf-8'), salt, iterations)
            return dk == stored_hash
        except Exception:
            return False

    # Fallback to bcrypt for legacy hashed passwords
    if hashed.startswith("$2b$") or hashed.startswith("$2a$"):
        try:
            import bcrypt
            return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
        except Exception as e:
            print(f"Bcrypt verification fallback failed: {e}")
            return False

    return False


def create_access_token(data: dict) -> str:
    """
    JWT = JSON Web Token. A signed string that encodes who the user is.
    Structure: header.payload.signature
    The server can verify its own signature without hitting the DB every request.
    """
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """
    Verify the JWT signature and return the payload.
    If the token was tampered with or expired, this raises a 401.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session invalid or expired. Please log in again."
        )


def get_current_user(access_token: str = Cookie(None)) -> dict:
    """
    FastAPI dependency  any route that needs a logged-in user injects this.
    FastAPI automatically reads the 'access_token' cookie from the request.
    """
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return decode_token(access_token)
