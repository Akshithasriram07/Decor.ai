from fastapi import APIRouter
from sqlalchemy import func, select
from app.api.deps import DB, CurrentUser
from app.models import Design, Wishlist, Order
router=APIRouter(prefix="/api/dashboard",tags=["Dashboard"])
@router.get("")
def dashboard(user:CurrentUser,db:DB):
    designs=db.scalar(select(func.count(Design.id)).where(Design.user_id==user.id)) or 0
    wishlist=db.scalar(select(func.count(Wishlist.id)).where(Wishlist.user_id==user.id)) or 0
    orders=db.scalar(select(func.count(Order.id)).where(Order.user_id==user.id)) or 0
    return {"saved_designs":designs,"wishlist":wishlist,"projects":0,"orders":orders}
