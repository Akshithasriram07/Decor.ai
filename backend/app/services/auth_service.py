from datetime import datetime, timedelta, timezone
from uuid import uuid4
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import User, VerificationCode, Notification
from app.core.security import hash_password, verify_password, random_code, hash_code, validate_password_strength
from app.services.email_service import send_email, EmailDeliveryError

def create_user(db: Session, name: str, email: str, password: str) -> tuple[User, str]:
    email = email.lower().strip()
    try:
        validate_password_strength(password)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(409, "An account with this email already exists")
    user = User(id=str(uuid4()), name=name.strip(), email=email, password_hash=hash_password(password), email_verified=False)
    db.add(user); db.flush()
    code = random_code()
    vc = VerificationCode(id=str(uuid4()), user_id=user.id, purpose="email_verification",
                          code_hash=hash_code(code), expires_at=datetime.now(timezone.utc)+timedelta(minutes=10))
    db.add(vc)
    db.add(Notification(id=str(uuid4()), user_id=user.id, title="Welcome to DecorAI",
                        message="Verify your email to unlock your private design studio."))
    db.commit(); db.refresh(user)
    try:
        send_email(
            email,
            "Your DecorAI verification code",
            f"Your DecorAI verification code is {code}. It expires in 10 minutes.",
        )
    except EmailDeliveryError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return user, code

def authenticate(db: Session, email: str, password: str) -> User:
    user = db.scalar(select(User).where(User.email == email.lower().strip()))
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")
    if not user.email_verified:
        raise HTTPException(403, "Please verify your email before signing in")
    return user

def issue_code(db: Session, user: User, purpose: str) -> str:
    db.execute(delete(VerificationCode).where(VerificationCode.user_id == user.id, VerificationCode.purpose == purpose))
    code = random_code()
    db.add(VerificationCode(id=str(uuid4()), user_id=user.id, purpose=purpose,
                            code_hash=hash_code(code), expires_at=datetime.now(timezone.utc)+timedelta(minutes=10)))
    db.commit()
    return code

def verify_code(db: Session, user: User, purpose: str, code: str):
    vc = db.scalar(select(VerificationCode).where(VerificationCode.user_id == user.id, VerificationCode.purpose == purpose)
                   .order_by(VerificationCode.created_at.desc()))
    now = datetime.now(timezone.utc)
    expires_at = (
        vc.expires_at.replace(tzinfo=timezone.utc)
        if vc and vc.expires_at.tzinfo is None
        else (vc.expires_at if vc else None)
    )
    if not vc or expires_at < now or vc.attempts >= 5:
        raise HTTPException(400, "The code is invalid or expired")
    if vc.code_hash != hash_code(code):
        vc.attempts += 1; db.commit()
        raise HTTPException(400, "Incorrect verification code")
    db.delete(vc); db.commit()
