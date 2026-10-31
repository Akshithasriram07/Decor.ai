from datetime import datetime, timezone
from sqlalchemy import String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class Design(Base):
    __tablename__ = "designs"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(180))
    room: Mapped[str] = mapped_column(String(80))
    style: Mapped[str] = mapped_column(String(80))
    image: Mapped[str] = mapped_column(String(1000))
    original_image: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(40), default="completed", index=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    user = relationship("User", back_populates="designs")
