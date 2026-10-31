from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from app.api.deps import DB, CurrentUser
from app.schemas.design import DesignResponse
from app.services.design_service import list_user_designs, get_user_design, delete_user_design, generate_design
from app.core.config import settings
from app.services.image_analysis import analyze_room_image

router = APIRouter(prefix="/api/designs", tags=["AI Designs"])
ALLOWED = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}

@router.get("", response_model=list[DesignResponse])
def designs(user: CurrentUser, db: DB): return list_user_designs(db, user.id)

@router.get("/{design_id}", response_model=DesignResponse)
def design(design_id: str, user: CurrentUser, db: DB):
    return get_user_design(db, user.id, design_id)

@router.post("/generate", response_model=DesignResponse, status_code=201)
async def generate(user: CurrentUser, db: DB, image: UploadFile = File(...),
                   room: str = Form("Living Room"), style: str = Form("Warm Modern"),
                   prompt: str | None = Form(None)):
    if image.content_type not in ALLOWED:
        raise HTTPException(400, "Only JPG, PNG or WEBP images are supported")
    content = await image.read()
    max_bytes = settings.max_upload_mb * 1024 * 1024
    if len(content) > max_bytes: raise HTTPException(413, f"Image exceeds {settings.max_upload_mb} MB")
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    path = Path(settings.upload_dir) / f"{user.id}_{uuid4()}{ALLOWED[image.content_type]}"
    path.write_bytes(content)
    try:
        return generate_design(db, user.id, path, room, style, prompt)
    except Exception as exc:
        if settings.environment == "development":
            raise HTTPException(502, f"AI generation failed: {exc}")
        raise HTTPException(502, "AI generation failed. Check your AI provider configuration.")


@router.post("/analyze")
async def analyze(user: CurrentUser, image: UploadFile = File(...),
                  room: str = Form("Living Room"), style: str = Form("Warm Modern"),
                  prompt: str | None = Form(None)):
    if image.content_type not in ALLOWED:
        raise HTTPException(400, "Only JPG, PNG or WEBP images are supported")
    content = await image.read()
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(413, f"Image exceeds {settings.max_upload_mb} MB")
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    path = Path(settings.upload_dir) / f"analysis_{user.id}_{uuid4()}{ALLOWED[image.content_type]}"
    path.write_bytes(content)
    try:
        return analyze_room_image(path, room, style, prompt)
    except Exception as exc:
        if settings.environment in {"development","dev","local"}:
            raise HTTPException(503, f"Local image analysis failed: {exc}") from exc
        raise HTTPException(503, "Local image analysis is temporarily unavailable.")

@router.delete("/{design_id}", status_code=204)
def delete(design_id: str, user: CurrentUser, db: DB): delete_user_design(db, user.id, design_id)
