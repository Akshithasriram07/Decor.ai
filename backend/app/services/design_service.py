from pathlib import Path
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Design
from app.ai.generator import get_generator
from app.core.config import settings

def list_user_designs(db: Session, user_id: str):
    return db.scalars(select(Design).where(Design.user_id == user_id).order_by(Design.created_at.desc())).all()

def get_user_design(db: Session, user_id: str, design_id: str):
    design = db.scalar(select(Design).where(Design.id == design_id, Design.user_id == user_id))
    if not design: raise HTTPException(status_code=404, detail="Design not found")
    return design

def delete_user_design(db: Session, user_id: str, design_id: str):
    design = get_user_design(db, user_id, design_id)
    db.delete(design); db.commit()

def generate_design(db: Session, user_id: str, source_path: Path, room: str, style: str, prompt: str | None):
    generator = get_generator()
    output_path = generator.generate(source_path, room, style, prompt)
    design = Design(
        id=str(uuid4()), user_id=user_id, title=style, room=room, style=style,
        image=f"/media/generated/{output_path.name}", original_image=f"/media/uploads/{source_path.name}",
        prompt=prompt, status="completed", is_public=False
    )
    db.add(design); db.commit(); db.refresh(design)
    return design
