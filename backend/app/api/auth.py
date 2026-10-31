from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.api.deps import DB, CurrentUser
from app.models import User
from app.schemas.auth import *
from app.services.auth_service import create_user, authenticate, issue_code, verify_code
from app.services.email_service import send_email, EmailDeliveryError
from app.core.security import create_access_token, hash_password, validate_password_strength

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/signup", response_model=UserResponse, status_code=201)
def signup(payload: SignUpRequest, db: DB):
    user, _ = create_user(db, payload.name, payload.email, payload.password)
    return user

@router.post("/verify-email")
def verify_email(payload: VerifyRequest, db: DB):
    user = db.scalar(select(User).where(User.email == payload.email.lower().strip()))
    if not user: return {"message": "If an account exists, verification was processed."}
    verify_code(db, user, "email_verification", payload.code)
    user.email_verified = True
    db.commit()
    return {"message": "Email verified successfully"}

@router.post("/resend-verification")
def resend(payload: ResendRequest, db: DB):
    user = db.scalar(select(User).where(User.email == payload.email.lower().strip()))
    if user and not user.email_verified:
        code = issue_code(db, user, "email_verification")
        try:
            send_email(
                user.email,
                "Your new DecorAI verification code",
                f"Your new verification code is {code}. It expires in 10 minutes.",
            )
        except EmailDeliveryError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {"message": "If the account is waiting for verification, a new code has been sent."}

@router.post("/signin", response_model=TokenResponse)
def signin(payload: SignInRequest, db: DB):
    user = authenticate(db, payload.email, payload.password)
    return {"access_token": create_access_token(user.id), "token_type": "bearer", "user": user}


@router.post("/demo-signin", response_model=TokenResponse)
def demo_signin(db: DB):
    """Development/demo account login. No credentials are required."""
    from app.core.config import settings
    if settings.environment.lower() not in {"development", "dev", "local", "test"}:
        raise HTTPException(404, "Demo sign-in is disabled in this environment")

    email = "demo@decorai.com"
    user = db.scalar(select(User).where(User.email == email))
    if not user:
        user = User(
            id="demo-user",
            name="Demo User",
            email=email,
            password_hash=hash_password("DemoOnly123!"),
            email_verified=True,
            role="user",
            plan="Free",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        user.email_verified = True
        db.commit()

    return {"access_token": create_access_token(user.id), "token_type": "bearer", "user": user}

@router.post("/forgot-password")
def forgot(payload: ForgotPasswordRequest, db: DB):
    user = db.scalar(select(User).where(User.email == payload.email.lower().strip()))
    if user:
        code = issue_code(db, user, "password_reset")
        try:
            send_email(
                user.email,
                "Reset your DecorAI password",
                f"Your password reset code is {code}. It expires in 10 minutes.",
            )
        except EmailDeliveryError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {"message": "If an account exists, a password reset code has been sent."}

@router.post("/reset-password")
def reset(payload: ResetPasswordRequest, db: DB):
    user = db.scalar(select(User).where(User.email == payload.email.lower().strip()))
    if not user: raise HTTPException(status_code=400, detail="Invalid reset request")
    verify_code(db, user, "password_reset", payload.code)
    try:
        validate_password_strength(payload.new_password)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    user.password_hash = hash_password(payload.new_password)
    db.commit()
    return {"message": "Password reset successfully"}

@router.get("/me", response_model=UserResponse)
def me(user: CurrentUser):
    return user
