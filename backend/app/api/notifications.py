from fastapi import APIRouter
from sqlalchemy import select
from app.api.deps import DB, CurrentUser
from app.models import Notification
router=APIRouter(prefix="/api/notifications",tags=["Notifications"])
@router.get("")
def notifications(user:CurrentUser,db:DB):
    rows=db.scalars(select(Notification).where(Notification.user_id==user.id).order_by(Notification.created_at.desc()).limit(50)).all()
    return [{"id":n.id,"title":n.title,"message":n.message,"read":n.read,"created_at":n.created_at.isoformat()} for n in rows]
@router.post("/{notification_id}/read")
def mark_read(notification_id:str,user:CurrentUser,db:DB):
    n=db.scalar(select(Notification).where(Notification.id==notification_id,Notification.user_id==user.id))
    if n: n.read=True; db.commit()
    return {"ok":True}
