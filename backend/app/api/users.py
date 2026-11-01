from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, File, HTTPException, UploadFile
from app.api.deps import DB, CurrentUser
from app.schemas.user import UserUpdate, UserResponse
from app.core.config import settings

router = APIRouter(prefix="/api/users", tags=["Users"])
AVATAR_TYPES = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}

@router.post("/me/avatar", response_model=UserResponse)
async def upload_avatar(user: CurrentUser, db: DB, image: UploadFile = File(...)):
    extension = AVATAR_TYPES.get(image.content_type or "")
    if not extension:
        raise HTTPException(400, "Only JPG, PNG or WEBP images are supported")
    content = await image.read()
    if not content:
        raise HTTPException(400, "The uploaded image is empty")
    max_bytes = settings.max_upload_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(413, f"Image exceeds {settings.max_upload_mb} MB")

    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    filename = f"avatar_{uuid4()}{extension}"
    (Path(settings.upload_dir) / filename).write_bytes(content)
    user.avatar = f"/media/uploads/{filename}"
    db.commit()
    db.refresh(user)
    return user

@router.get("/me", response_model=UserResponse)
def get_me(user: CurrentUser): return user

@router.put("/me", response_model=UserResponse)
def update_me(payload: UserUpdate, db: DB, user: CurrentUser):
    for key, value in payload.model_dump(exclude_unset=True).items(): setattr(user, key, value)
    db.commit(); db.refresh(user)
    return user
