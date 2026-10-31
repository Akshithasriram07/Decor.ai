from pydantic import BaseModel, EmailStr, Field

class SignUpRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class SignInRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class VerifyRequest(BaseModel):
    email: EmailStr
    code: str = Field(min_length=6, max_length=6)

class ResendRequest(BaseModel):
    email: EmailStr

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    code: str = Field(min_length=6, max_length=6)
    new_password: str = Field(min_length=8, max_length=128)

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    plan: str
    location: str
    avatar: str | None = None
    email_verified: bool
    model_config = {"from_attributes": True}

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
