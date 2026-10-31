from pydantic import BaseModel, EmailStr, Field

class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    location: str | None = Field(default=None, max_length=120)
    avatar: str | None = Field(default=None, max_length=500)

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    plan: str
    role: str = "user"
    location: str
    avatar: str | None = None
    model_config = {"from_attributes": True}
