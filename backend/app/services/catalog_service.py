from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from app.models import Product, Worker

def search_products(db: Session, q: str = "", category: str = "All"):
    stmt = select(Product).where(Product.available.is_(True))
    if category != "All": stmt = stmt.where(Product.category == category)
    if q: stmt = stmt.where(or_(Product.name.ilike(f"%{q}%"), Product.category.ilike(f"%{q}%"), Product.brand.ilike(f"%{q}%")))
    rows = db.scalars(stmt.order_by(Product.name)).all()
    seen = set(); unique = []
    for row in rows:
        key = (row.image or "").strip().lower() or (row.name.strip().lower(), row.category.strip().lower())
        if key in seen: continue
        seen.add(key); unique.append(row)
    return unique

def search_workers(db: Session, q: str = "", role: str = "All", location: str = ""):
    stmt = select(Worker).where(Worker.available.is_(True))
    if role != "All": stmt = stmt.where(Worker.role == role)
    if location: stmt = stmt.where(Worker.location.ilike(f"%{location}%"))
    if q: stmt = stmt.where(or_(Worker.name.ilike(f"%{q}%"), Worker.role.ilike(f"%{q}%"), Worker.location.ilike(f"%{q}%")))
    rows = db.scalars(stmt.order_by(Worker.rating.desc())).all()
    seen = set(); unique = []
    for row in rows:
        key = (row.image or "").strip().lower() or (row.name.strip().lower(), row.role.strip().lower(), row.location.strip().lower())
        if key in seen: continue
        seen.add(key); unique.append(row)
    return unique
