from fastapi import APIRouter, Query, HTTPException
from app.api.deps import DB, CurrentUser
from app.models import Design
from app.schemas.design import DesignResponse
from sqlalchemy import select, or_

router = APIRouter(prefix="/api/explore", tags=["Explore"])

@router.get("", response_model=list[DesignResponse])
def explore(user: CurrentUser, db: DB, q: str = Query(""), room: str = Query("All"), style: str = Query("All")):
    stmt = select(Design).where(Design.status == "completed", Design.is_public.is_(True))
    if room != "All": stmt = stmt.where(Design.room == room)
    if style != "All": stmt = stmt.where(Design.style == style)
    if q: stmt = stmt.where(or_(Design.title.ilike(f"%{q}%"), Design.room.ilike(f"%{q}%"), Design.style.ilike(f"%{q}%")))
    rows = db.scalars(stmt.order_by(Design.created_at.desc()).limit(100)).all()
    seen = set(); unique = []
    for row in rows:
        key = (row.image or "").strip().lower() or (row.title.strip().lower(), row.room.strip().lower(), row.style.strip().lower())
        if key in seen: continue
        seen.add(key); unique.append(row)
    return unique

@router.get("/{design_id}", response_model=DesignResponse)
def explore_detail(design_id: str, user: CurrentUser, db: DB):
    item = db.scalar(select(Design).where(Design.id == design_id, Design.is_public.is_(True)))
    if not item: raise HTTPException(404, "Design not found")
    return item
