from uuid import uuid4
from fastapi import APIRouter, HTTPException
from sqlalchemy import func, select
from app.api.deps import DB, CurrentUser
from app.models import User, Design, Product, Worker, WorkerApplication, Order

router = APIRouter(prefix="/api/admin", tags=["Admin"])


def require_admin(user: User):
    if getattr(user, "role", "user") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")


@router.get("/overview")
def overview(user: CurrentUser, db: DB):
    require_admin(user)
    return {
        "users": db.scalar(select(func.count(User.id))) or 0,
        "verified_users": db.scalar(select(func.count(User.id)).where(User.email_verified.is_(True))) or 0,
        "designs": db.scalar(select(func.count(Design.id))) or 0,
        "public_designs": db.scalar(select(func.count(Design.id)).where(Design.is_public.is_(True))) or 0,
        "products": db.scalar(select(func.count(Product.id))) or 0,
        "workers": db.scalar(select(func.count(Worker.id))) or 0,
        "pending_worker_applications": db.scalar(select(func.count(WorkerApplication.id)).where(WorkerApplication.status == "pending")) or 0,
        "orders": db.scalar(select(func.count(Order.id))) or 0,
        "paid_orders": db.scalar(select(func.count(Order.id)).where(Order.status == "paid")) or 0,
        "revenue": db.scalar(select(func.coalesce(func.sum(Order.total), 0)).where(Order.status == "paid")) or 0,
    }


@router.get("/users")
def users(user: CurrentUser, db: DB):
    require_admin(user)
    rows = db.scalars(select(User).order_by(User.created_at.desc()).limit(200)).all()
    return [{
        "id": x.id, "name": x.name, "email": x.email, "role": getattr(x, "role", "user"),
        "verified": x.email_verified, "plan": x.plan, "created_at": x.created_at.isoformat()
    } for x in rows]


@router.get("/designs")
def designs(user: CurrentUser, db: DB):
    require_admin(user)
    rows = db.scalars(select(Design).order_by(Design.created_at.desc()).limit(200)).all()
    return [{
        "id": x.id, "title": x.title, "room": x.room, "style": x.style,
        "image": x.image, "public": x.is_public, "status": x.status,
        "created_at": x.created_at.isoformat(), "user_id": x.user_id
    } for x in rows]


@router.patch("/designs/{design_id}/visibility")
def design_visibility(design_id: str, public: bool, user: CurrentUser, db: DB):
    require_admin(user)
    design = db.get(Design, design_id)
    if not design:
        raise HTTPException(404, "Design not found")
    design.is_public = public
    db.commit()
    return {"id": design.id, "public": design.is_public}


@router.get("/orders")
def orders(user: CurrentUser, db: DB):
    require_admin(user)
    rows = db.scalars(select(Order).order_by(Order.created_at.desc()).limit(200)).all()
    return [{
        "id": x.id, "user_id": x.user_id, "total": x.total, "status": x.status,
        "payment_provider": x.payment_provider, "payment_reference": x.payment_reference,
        "shipping_name": x.shipping_name, "shipping_phone": x.shipping_phone,
        "created_at": x.created_at.isoformat()
    } for x in rows]


@router.patch("/orders/{order_id}/status")
def order_status(order_id: str, status: str, user: CurrentUser, db: DB):
    require_admin(user)
    allowed = {"pending", "paid", "processing", "shipped", "delivered", "cancelled"}
    if status not in allowed:
        raise HTTPException(400, f"Status must be one of: {', '.join(sorted(allowed))}")
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(404, "Order not found")
    order.status = status
    db.commit()
    return {"id": order.id, "status": order.status}


@router.get("/workers")
def workers(user: CurrentUser, db: DB):
    require_admin(user)
    rows = db.scalars(select(Worker).order_by(Worker.name)).all()
    return [{
        "id": x.id, "name": x.name, "role": x.role, "location": x.location,
        "rating": x.rating, "jobs": x.jobs, "available": x.available
    } for x in rows]


@router.patch("/workers/{worker_id}/availability")
def worker_availability(worker_id: str, available: bool, user: CurrentUser, db: DB):
    require_admin(user)
    worker = db.get(Worker, worker_id)
    if not worker:
        raise HTTPException(404, "Worker not found")
    worker.available = available
    db.commit()
    return {"id": worker.id, "available": worker.available}


@router.get("/worker-applications")
def worker_applications(user: CurrentUser, db: DB):
    require_admin(user)
    rows = db.scalars(select(WorkerApplication).order_by(WorkerApplication.created_at.desc()).limit(200)).all()
    return [{
        "id": x.id, "user_id": x.user_id, "role": x.role, "location": x.location,
        "phone": x.phone, "experience": x.experience, "bio": x.bio,
        "portfolio_url": x.portfolio_url, "status": x.status,
        "created_at": x.created_at.isoformat()
    } for x in rows]


@router.patch("/worker-applications/{application_id}")
def worker_application_status(application_id: str, status: str, user: CurrentUser, db: DB):
    require_admin(user)
    if status not in {"pending", "approved", "rejected"}:
        raise HTTPException(400, "Invalid application status")
    item = db.get(WorkerApplication, application_id)
    if not item:
        raise HTTPException(404, "Application not found")
    item.status = status
    if status == "approved":
        existing = db.scalar(select(Worker).where(Worker.email == db.get(User, item.user_id).email))
        if not existing:
            owner = db.get(User, item.user_id)
            worker = Worker(
                id=str(uuid4()), name=owner.name, role=item.role, location=item.location,
                rating=5.0, jobs=0, image=owner.avatar or "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=700&q=90",
                phone=item.phone, email=owner.email, description=item.bio, available=True
            )
            db.add(worker)
    db.commit()
    return {"id": item.id, "status": item.status}
