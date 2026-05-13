from datetime import datetime, date, timezone
from sqlalchemy import Integer, String, Boolean, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    checkins: Mapped[list["Checkin"]] = relationship(back_populates="habit", cascade="all, delete-orphan")


class Checkin(Base):
    __tablename__ = "checkins"
    __table_args__ = (UniqueConstraint("habit_id", "checked_in_on"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    habit_id: Mapped[int] = mapped_column(Integer, ForeignKey("habits.id"), nullable=False)
    checked_in_on: Mapped[date] = mapped_column(Date, nullable=False)
    note: Mapped[str | None] = mapped_column(String(500))

    habit: Mapped["Habit"] = relationship(back_populates="checkins")
