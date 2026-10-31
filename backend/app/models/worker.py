from sqlalchemy import String, Integer, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class Worker(Base):
    __tablename__ = "workers"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(180), index=True)
    role: Mapped[str] = mapped_column(String(100), index=True)
    location: Mapped[str] = mapped_column(String(120), index=True)
    rating: Mapped[float] = mapped_column(Float, default=4.8)
    jobs: Mapped[int] = mapped_column(Integer, default=0)
    image: Mapped[str] = mapped_column(String(1000))
    phone: Mapped[str | None] = mapped_column(String(40), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(String(800), default="")
    available: Mapped[bool] = mapped_column(Boolean, default=True)
