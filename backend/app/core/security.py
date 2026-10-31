from datetime import datetime, timedelta, timezone
import hashlib, secrets
import jwt
from pwdlib import PasswordHash
from app.core.config import settings

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)

def create_access_token(user_id: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub": user_id, "exp": exp}, settings.secret_key, algorithm="HS256")

def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Token subject missing")
        return str(user_id)
    except (jwt.PyJWTError, ValueError) as exc:
        raise ValueError("Invalid or expired access token") from exc

def random_code() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"

def hash_code(code: str) -> str:
    return hashlib.sha256(f"{settings.secret_key}:{code}".encode()).hexdigest()


def validate_password_strength(password: str) -> None:
    """Require a strong password for account creation and password reset."""
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters.")
    if not any(c.isupper() for c in password):
        raise ValueError("Password must contain at least one uppercase letter.")
    if not any(c.islower() for c in password):
        raise ValueError("Password must contain at least one lowercase letter.")
    if not any(c.isdigit() for c in password):
        raise ValueError("Password must contain at least one number.")
    if not any(not c.isalnum() for c in password):
        raise ValueError("Password must contain at least one special character.")
