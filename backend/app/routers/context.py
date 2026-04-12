"""Context data endpoints: health events, mood check-ins, calendar."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CalendarEvent, HealthEvent, MoodCheckin
from app.schemas import (
    CalendarEventOut,
    HealthEventCreate,
    HealthEventOut,
    MoodCreate,
    MoodOut,
)

router = APIRouter(prefix="/api", tags=["context"])


# ── Health Events ───────────────────────────────────────────────────────


@router.post("/health/{user_id}", response_model=HealthEventOut)
def log_workout(user_id: str, body: HealthEventCreate, db: Session = Depends(get_db)):
    event = HealthEvent(
        user_id=user_id,
        event_type="workout",
        activity_type=body.activity_type,
        duration_minutes=body.duration_minutes,
        distance_km=body.distance_km,
        calories=body.calories,
        avg_heart_rate=body.avg_heart_rate,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.get("/health/{user_id}", response_model=list[HealthEventOut])
def list_workouts(user_id: str, db: Session = Depends(get_db)):
    return (
        db.query(HealthEvent)
        .filter(HealthEvent.user_id == user_id)
        .order_by(HealthEvent.timestamp.desc())
        .limit(10)
        .all()
    )


# ── Mood ────────────────────────────────────────────────────────────────


@router.post("/mood/{user_id}", response_model=MoodOut)
def log_mood(user_id: str, body: MoodCreate, db: Session = Depends(get_db)):
    checkin = MoodCheckin(user_id=user_id, mood=body.mood)
    db.add(checkin)
    db.commit()
    db.refresh(checkin)
    return checkin


# ── Calendar ────────────────────────────────────────────────────────────


@router.get("/calendar/{user_id}", response_model=list[CalendarEventOut])
def list_calendar(user_id: str, db: Session = Depends(get_db)):
    return (
        db.query(CalendarEvent)
        .filter(CalendarEvent.user_id == user_id)
        .order_by(CalendarEvent.event_date)
        .all()
    )
