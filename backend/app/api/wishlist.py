from uuid import uuid4
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.api.deps import DB, CurrentUser
from app.models import Wishlist, Product
from app.schemas.catalog import ProductResponse

router = APIRouter(prefix="/api/wishlist", tags=["Wishlist"])

@router.get("", response_model=list[ProductResponse])
def wishlist(user: CurrentUser, db: DB):
    rows = db.scalars(select(Wishlist).where(Wishlist.user_id == user.id).order_by(Wishlist.created_at.desc())).all()
    return [r.product for r in rows if r.product]

@router.post("/{product_id}", response_model=ProductResponse)
def add(product_id: str, user: CurrentUser, db: DB):
    product = db.get(Product, product_id)
    if not product: raise HTTPException(404, "Product not found")
    existing = db.scalar(select(Wishlist).where(Wishlist.user_id == user.id, Wishlist.product_id == product_id))
    if not existing:
        db.add(Wishlist(id=str(uuid4()), user_id=user.id, product_id=product_id)); db.commit()
    return product

@router.delete("/{product_id}", status_code=204)
def remove(product_id: str, user: CurrentUser, db: DB):
    row = db.scalar(select(Wishlist).where(Wishlist.user_id == user.id, Wishlist.product_id == product_id))
    if row: db.delete(row); db.commit()
