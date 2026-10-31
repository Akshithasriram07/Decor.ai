from uuid import uuid4
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.api.deps import DB, CurrentUser
from app.models import CartItem, Product
from app.schemas.cart import *

router = APIRouter(prefix="/api/cart", tags=["Cart"])

def cart_payload(db, user_id):
    rows = db.scalars(select(CartItem).where(CartItem.user_id == user_id).order_by(CartItem.created_at.desc())).all()
    items=[]; subtotal=0
    for row in rows:
        if not row.product: continue
        line=row.product.price*row.quantity; subtotal += line
        items.append({"id":row.id,"product_id":row.product_id,"quantity":row.quantity,"name":row.product.name,
                      "price":row.product.price,"image":row.product.image,"line_total":line})
    shipping = 0 if subtotal >= 50000 or subtotal == 0 else 499
    return {"items":items,"subtotal":subtotal,"shipping":shipping,"total":subtotal+shipping}

@router.get("", response_model=CartResponse)
def get_cart(user: CurrentUser, db: DB): return cart_payload(db,user.id)

@router.post("/items", response_model=CartResponse)
def add(payload: CartAdd, user: CurrentUser, db: DB):
    product=db.get(Product,payload.product_id)
    if not product or not product.available: raise HTTPException(404,"Product unavailable")
    row=db.scalar(select(CartItem).where(CartItem.user_id==user.id,CartItem.product_id==payload.product_id))
    if row: row.quantity=min(20,row.quantity+payload.quantity)
    else: db.add(CartItem(id=str(uuid4()),user_id=user.id,product_id=payload.product_id,quantity=payload.quantity))
    db.commit(); return cart_payload(db,user.id)

@router.patch("/items/{item_id}", response_model=CartResponse)
def update(item_id: str, payload: CartUpdate, user: CurrentUser, db: DB):
    row=db.scalar(select(CartItem).where(CartItem.id==item_id,CartItem.user_id==user.id))
    if not row: raise HTTPException(404,"Cart item not found")
    row.quantity=payload.quantity; db.commit(); return cart_payload(db,user.id)

@router.delete("/items/{item_id}", response_model=CartResponse)
def remove(item_id: str, user: CurrentUser, db: DB):
    row=db.scalar(select(CartItem).where(CartItem.id==item_id,CartItem.user_id==user.id))
    if row: db.delete(row); db.commit()
    return cart_payload(db,user.id)
