from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.db.session import Base, engine
from app.models import User, Design, Product, Worker, Wishlist, CartItem, Order, OrderItem, Notification, VerificationCode, WorkerApplication
from app.api import auth, users, designs, explore, catalog, wishlist, dashboard
from app.api import cart, orders, notifications, workers, admin
from sqlalchemy import text

Path(settings.upload_dir).mkdir(parents=True,exist_ok=True)
Path(settings.generated_dir).mkdir(parents=True,exist_ok=True)
Base.metadata.create_all(bind=engine)

# Lightweight development migration for existing SQLite databases created by older DecorAI builds.
with engine.begin() as connection:
    if settings.database_url.startswith("sqlite"):
        columns = {row[1] for row in connection.execute(text("PRAGMA table_info(users)"))}
        if "role" not in columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(30) DEFAULT 'user'"))

app=FastAPI(title=settings.app_name,version="4.1.0",description="DecorAI end-to-end API")
app.add_middleware(CORSMiddleware,allow_origins=settings.origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.mount("/media/uploads",StaticFiles(directory=settings.upload_dir),name="uploads")
app.mount("/media/generated",StaticFiles(directory=settings.generated_dir),name="generated")
for router in [auth.router,users.router,designs.router,explore.router,catalog.router,wishlist.router,dashboard.router,cart.router,orders.router,notifications.router,workers.router, admin.router]:
    app.include_router(router)
@app.get("/")
def root(): return {"name":"DecorAI API","status":"running","docs":"/docs"}
@app.get("/health")
def health(): return {"status":"ok","service":"decorai-backend"}
