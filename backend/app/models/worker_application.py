from datetime import datetime, timezone
from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class WorkerApplication(Base):
    __tablename__ = "worker_applications"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    role: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(120))
    phone: Mapped[str] = mapped_column(String(40))
    experience: Mapped[str] = mapped_column(String(100))
    bio: Mapped[str] = mapped_column(Text)
    portfolio_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    status: Mapped[str] = mapped_column(String(40), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
