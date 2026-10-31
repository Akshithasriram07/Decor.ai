from fastapi import APIRouter
from app.api.deps import DB, CurrentUser
from app.schemas.user import UserUpdate, UserResponse

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_me(user: CurrentUser): return user

@router.put("/me", response_model=UserResponse)
def update_me(payload: UserUpdate, db: DB, user: CurrentUser):
    for key, value in payload.model_dump(exclude_unset=True).items(): setattr(user, key, value)
    db.commit(); db.refresh(user)
    return user
