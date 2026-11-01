from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import User, VerificationCode, Notification
from app.core.security import (
    hash_password,
    verify_password,
    random_code,
    hash_code,
    validate_password_strength,
)
from app.services.email_service import send_email, EmailDeliveryError


def create_user(
    db: Session,
    name: str,
    email: str,
    password: str
) -> tuple[User, str]:

    email = email.lower().strip()

    try:
        validate_password_strength(password)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc)
        ) from exc

    existing_user = db.scalar(
        select(User).where(User.email == email)
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists"
        )

    try:
        user = User(
            id=str(uuid4()),
            name=name.strip(),
            email=email,
            password_hash=hash_password(password),
            email_verified=False
        )

        db.add(user)
        db.flush()

        code = random_code()

        verification = VerificationCode(
            id=str(uuid4()),
            user_id=user.id,
            purpose="email_verification",
            code_hash=hash_code(code),
            expires_at=(
                datetime.now(timezone.utc) + timedelta(minutes=10)
            )
        )

        db.add(verification)

        notification = Notification(
            id=str(uuid4()),
            user_id=user.id,
            title="Welcome to DecorAI",
            message="Verify your email to unlock your private design studio."
        )

        db.add(notification)

        # Send before committing, so failed delivery does not leave
        # an unverified account in the database.
        send_email(
            email,
            "Your DecorAI verification code",
            f"Your DecorAI verification code is {code}. "
            "It expires in 10 minutes.",
        )

        db.commit()
        db.refresh(user)

        return user, code

    except EmailDeliveryError as exc:
        db.rollback()
        raise HTTPException(
            status_code=503,
            detail=str(exc)
        ) from exc

    except Exception:
        db.rollback()
        raise


def authenticate(
    db: Session,
    email: str,
    password: str
) -> User:

    user = db.scalar(
        select(User).where(
            User.email == email.lower().strip()
        )
    )

    if not user or not verify_password(
        password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not user.email_verified:
        raise HTTPException(
            status_code=403,
            detail="Please verify your email before signing in"
        )

    return user


def issue_code(
    db: Session,
    user: User,
    purpose: str
) -> str:

    db.execute(
        delete(VerificationCode).where(
            VerificationCode.user_id == user.id,
            VerificationCode.purpose == purpose
        )
    )

    code = random_code()

    verification = VerificationCode(
        id=str(uuid4()),
        user_id=user.id,
        purpose=purpose,
        code_hash=hash_code(code),
        expires_at=(
            datetime.now(timezone.utc) + timedelta(minutes=10)
        )
    )

    db.add(verification)
    db.commit()

    return code


def verify_code(
    db: Session,
    user: User,
    purpose: str,
    code: str
):
    verification = db.scalar(
        select(VerificationCode).where(
            VerificationCode.user_id == user.id,
            VerificationCode.purpose == purpose
        ).order_by(
            VerificationCode.created_at.desc()
        )
    )

    now = datetime.now(timezone.utc)

    expires_at = None

    if verification:
        expires_at = (
            verification.expires_at.replace(tzinfo=timezone.utc)
            if verification.expires_at.tzinfo is None
            else verification.expires_at
        )

    if (
        not verification
        or expires_at < now
        or verification.attempts >= 5
    ):
        raise HTTPException(
            status_code=400,
            detail="The code is invalid or expired"
        )

    if verification.code_hash != hash_code(code):
        verification.attempts += 1
        db.commit()

        raise HTTPException(
            status_code=400,
            detail="Incorrect verification code"
        )

    db.delete(verification)
    db.commit()