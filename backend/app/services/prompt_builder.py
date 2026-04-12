"""Build the dynamic system prompt from the user's Voices and context."""

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models import CalendarEvent, Guideline, HealthEvent, MoodCheckin, Voice

MOOD_LABELS = {1: "rough", 2: "not great", 3: "okay", 4: "good", 5: "great"}


def build_system_prompt(db: Session, user_id: str) -> tuple[str, list[dict]]:
    """Return (system_prompt, guideline_records) for the given user.

    guideline_records is a list of dicts with voice info, used for attribution.
    """
    voices = db.query(Voice).filter(Voice.user_id == user_id).all()
    voice_map = {v.id: v for v in voices}

    guidelines = (
        db.query(Guideline)
        .filter(Guideline.user_id == user_id, Guideline.active.is_(True))
        .all()
    )

    # Group guidelines by voice
    by_voice: dict[str | None, list[Guideline]] = {}
    for g in guidelines:
        by_voice.setdefault(g.voice_id, []).append(g)

    prompt_parts = [
        "You are Compass, a personal assistant that channels the guidance of "
        "the user's trusted Voices -- real people who know the user and have "
        "deposited their wisdom into this system.\n\n"
        "CORE PRINCIPLE: You are a mediator, not an advisor. Your responses "
        "should reflect what the user's Voices have told you, not your own "
        "training data. When you have no relevant guidance from a Voice, say so "
        'and suggest the user ask the appropriate person.\n\n'
        "ONLY reference information explicitly provided in the guidance and "
        "context below. NEVER infer, guess, or elaborate beyond what is stated.\n",
    ]

    # Trusted voice guidelines
    for voice_id, rules in by_voice.items():
        if voice_id is None:
            continue
        voice = voice_map.get(voice_id)
        if not voice:
            continue
        safety = [r for r in rules if r.is_safety]
        advisory = [r for r in rules if not r.is_safety]
        prompt_parts.append(f"\n[{voice.icon} {voice.name} -- {voice.role.title()}]")
        for r in safety:
            prompt_parts.append(f"  SAFETY: {r.guideline_text}")
        for r in advisory:
            prompt_parts.append(f"  - {r.guideline_text}")

    # Platform defaults
    platform = by_voice.get(None, [])
    if platform:
        prompt_parts.append("\n[⚙️ Compass Defaults -- Always Active]")
        for r in platform:
            prompt_parts.append(f"  - {r.guideline_text}")

    # Context: recent health events (use naive datetimes -- SQLite stores without tz)
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    recent_workouts = (
        db.query(HealthEvent)
        .filter(
            HealthEvent.user_id == user_id,
            HealthEvent.timestamp >= today_start - timedelta(days=1),
        )
        .order_by(HealthEvent.timestamp.desc())
        .limit(3)
        .all()
    )
    if recent_workouts:
        prompt_parts.append("\n[RECENT ACTIVITY]")
        for w in recent_workouts:
            line = f"  - {w.activity_type or w.event_type}"
            if w.duration_minutes:
                line += f", {int(w.duration_minutes)} minutes"
            if w.distance_km:
                line += f", {w.distance_km:.1f} km"
            if w.calories:
                line += f", {int(w.calories)} cal"
            prompt_parts.append(line)

    # Context: mood
    latest_mood = (
        db.query(MoodCheckin)
        .filter(MoodCheckin.user_id == user_id, MoodCheckin.timestamp >= today_start)
        .order_by(MoodCheckin.timestamp.desc())
        .first()
    )
    if latest_mood:
        label = MOOD_LABELS.get(latest_mood.mood, "neutral")
        prompt_parts.append(f"\n[MOOD TODAY]\n  User is feeling: {label}")

    # Context: upcoming calendar
    upcoming = (
        db.query(CalendarEvent)
        .filter(
            CalendarEvent.user_id == user_id,
            CalendarEvent.event_date >= now,
            CalendarEvent.event_date <= now + timedelta(days=14),
        )
        .order_by(CalendarEvent.event_date)
        .limit(5)
        .all()
    )
    if upcoming:
        prompt_parts.append("\n[UPCOMING CALENDAR]")
        for ev in upcoming:
            days_away = (ev.event_date - now).days
            when = "today" if days_away == 0 else f"in {days_away} days"
            line = f"  - {ev.title} ({when})"
            if ev.notes:
                line += f" -- {ev.notes}"
            prompt_parts.append(line)

    # Attribution and tone rules
    prompt_parts.append(
        "\nATTRIBUTION: When your response is shaped by a Voice's guidance, "
        'reference them naturally: "Your doctor recommended..." or '
        '"Coach Mike mentioned..." Do not cite guidelines mechanically.'
        "\n\nNever shame, guilt-trip, or talk down to the user."
    )

    # Build guideline records for attribution tracking
    guideline_records = []
    for g in guidelines:
        voice = voice_map.get(g.voice_id) if g.voice_id else None
        guideline_records.append(
            {
                "id": g.id,
                "voice_name": voice.name if voice else "Compass Defaults",
                "voice_icon": voice.icon if voice else "⚙️",
                "guideline_text": g.guideline_text,
                "domain": g.domain,
                "is_safety": g.is_safety,
            }
        )

    return "\n".join(prompt_parts), guideline_records
