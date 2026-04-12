"""CRUD endpoints for guidelines and voices."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Guideline, Voice
from app.schemas import (
    GuidanceOverview,
    GuidelineCreate,
    GuidelineOut,
    VoiceOut,
)

router = APIRouter(prefix="/api", tags=["guidelines"])


# ── Voices ──────────────────────────────────────────────────────────────


@router.get("/voices/{user_id}", response_model=list[VoiceOut])
def list_voices(user_id: str, db: Session = Depends(get_db)):
    return db.query(Voice).filter(Voice.user_id == user_id).all()


# ── Guidelines ──────────────────────────────────────────────────────────


@router.get("/guidelines/{user_id}", response_model=list[GuidelineOut])
def list_guidelines(
    user_id: str,
    voice_id: str | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(Guideline).filter(
        Guideline.user_id == user_id, Guideline.active.is_(True)
    )
    if voice_id:
        q = q.filter(Guideline.voice_id == voice_id)
    return q.order_by(Guideline.created_at).all()


@router.post("/guidelines/{user_id}/{voice_id}", response_model=GuidelineOut)
def create_guideline(
    user_id: str,
    voice_id: str,
    body: GuidelineCreate,
    db: Session = Depends(get_db),
):
    voice = db.query(Voice).filter(Voice.id == voice_id).first()
    if not voice:
        raise HTTPException(404, "Voice not found")

    g = Guideline(
        user_id=user_id,
        voice_id=voice_id,
        author_name=voice.name,
        author_role="trusted",
        domain=body.domain,
        guideline_text=body.guideline_text,
        is_safety=body.is_safety,
    )
    db.add(g)
    db.commit()
    db.refresh(g)
    return g


@router.delete("/guidelines/{guideline_id}")
def delete_guideline(guideline_id: str, db: Session = Depends(get_db)):
    g = db.query(Guideline).filter(Guideline.id == guideline_id).first()
    if not g:
        raise HTTPException(404, "Guideline not found")
    db.delete(g)
    db.commit()
    return {"ok": True}


# ── Overview (all guidance for a user) ──────────────────────────────────


@router.get("/overview/{user_id}", response_model=GuidanceOverview)
def get_overview(user_id: str, db: Session = Depends(get_db)):
    voices = db.query(Voice).filter(Voice.user_id == user_id).all()
    guidelines = (
        db.query(Guideline)
        .filter(Guideline.user_id == user_id, Guideline.active.is_(True))
        .all()
    )

    by_voice: dict[str | None, list[Guideline]] = {}
    for g in guidelines:
        by_voice.setdefault(g.voice_id, []).append(g)

    voice_sections = []
    for v in voices:
        voice_sections.append(
            GuidanceOverview.VoiceGuidance(
                voice=v,  # type: ignore[arg-type]
                guidelines=by_voice.get(v.id, []),  # type: ignore[arg-type]
            )
        )

    platform = by_voice.get(None, [])
    platform_texts = [g.guideline_text for g in platform]

    return GuidanceOverview(voices=voice_sections, platform_defaults=platform_texts)
