import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def _uuid() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return datetime.utcnow()


class Voice(Base):
    """A trusted person (Voice) who provides guidance for a user."""

    __tablename__ = "voices"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String, index=True)
    name: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)  # doctor, caregiver, coach, family
    domains: Mapped[str] = mapped_column(String)  # comma-separated: "health,medications"
    icon: Mapped[str] = mapped_column(String, default="👤")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class Guideline(Base):
    """A piece of guidance from a Voice, the user, or the platform."""

    __tablename__ = "guidelines"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String, index=True)
    voice_id: Mapped[str | None] = mapped_column(String, nullable=True)
    author_name: Mapped[str] = mapped_column(String)
    author_role: Mapped[str] = mapped_column(String)  # user, trusted, platform
    domain: Mapped[str] = mapped_column(String)
    guideline_text: Mapped[str] = mapped_column(Text)
    is_safety: Mapped[bool] = mapped_column(Boolean, default=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    organization_id: Mapped[str | None] = mapped_column(String, nullable=True)
    recommended_llm: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class HealthEvent(Base):
    """A health/fitness event (workout, steps, etc.)."""

    __tablename__ = "health_events"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String, index=True)
    event_type: Mapped[str] = mapped_column(String)  # workout, steps, etc.
    activity_type: Mapped[str | None] = mapped_column(String, nullable=True)
    duration_minutes: Mapped[float | None] = mapped_column(Float, nullable=True)
    distance_km: Mapped[float | None] = mapped_column(Float, nullable=True)
    calories: Mapped[float | None] = mapped_column(Float, nullable=True)
    avg_heart_rate: Mapped[int | None] = mapped_column(Integer, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=_now)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class CalendarEvent(Base):
    """A calendar event (real or seed data)."""

    __tablename__ = "calendar_events"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String, index=True)
    title: Mapped[str] = mapped_column(String)
    event_date: Mapped[datetime] = mapped_column(DateTime)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class MoodCheckin(Base):
    """A mood check-in from the user."""

    __tablename__ = "mood_checkins"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String, index=True)
    mood: Mapped[int] = mapped_column(Integer)  # 1-5 scale
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=_now)
