from fastapi import APIRouter, Query, HTTPException
from sqlalchemy import select
from app.api.deps import DB, CurrentUser
from app.schemas.catalog import ProductResponse, WorkerResponse
from app.services.catalog_service import search_products, search_workers
from app.models import Product, Worker

router = APIRouter(tags=["Catalog"])

@router.get("/api/products", response_model=list[ProductResponse])
def products(user: CurrentUser, db: DB, q: str = Query(""), category: str = Query("All")):
    return search_products(db, q, category)

@router.get("/api/products/{product_id}", response_model=ProductResponse)
def product(product_id: str, user: CurrentUser, db: DB):
    item = db.get(Product, product_id)
    if not item: raise HTTPException(404, "Product not found")
    return item

@router.get("/api/workers", response_model=list[WorkerResponse])
def workers(user: CurrentUser, db: DB, q: str = Query(""), role: str = Query("All"), location: str = Query("")):
    return search_workers(db, q, role, location)

@router.get("/api/workers/{worker_id}", response_model=WorkerResponse)
def worker(worker_id: str, user: CurrentUser, db: DB):
    item = db.get(Worker, worker_id)
    if not item: raise HTTPException(404, "Worker not found")
    return item
