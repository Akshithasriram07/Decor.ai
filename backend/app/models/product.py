from sqlalchemy import String, Integer, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class Product(Base):
    __tablename__ = "products"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(180), index=True)
    category: Mapped[str] = mapped_column(String(80), index=True)
    price: Mapped[int] = mapped_column(Integer)
    image: Mapped[str] = mapped_column(String(1000))
    description: Mapped[str] = mapped_column(String(600), default="")
    brand: Mapped[str] = mapped_column(String(120), default="DecorAI Select")
    rating: Mapped[float] = mapped_column(Float, default=4.8)
    available: Mapped[bool] = mapped_column(Boolean, default=True)
