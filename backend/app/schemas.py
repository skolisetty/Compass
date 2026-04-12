from datetime import datetime

from pydantic import BaseModel


class VoiceOut(BaseModel):
    id: str
    user_id: str
    name: str
    role: str
    domains: str
    icon: str
    created_at: datetime

    model_config = {"from_attributes": True}


class GuidelineCreate(BaseModel):
    guideline_text: str
    domain: str = "all"
    is_safety: bool = False


class GuidelineOut(BaseModel):
    id: str
    user_id: str
    voice_id: str | None
    author_name: str
    author_role: str
    domain: str
    guideline_text: str
    is_safety: bool
    active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class AskRequest(BaseModel):
    question: str
    user_id: str


class Attribution(BaseModel):
    voice_name: str
    voice_icon: str
    guideline_text: str


class AskResponse(BaseModel):
    answer: str
    attributions: list[Attribution]


class HealthEventCreate(BaseModel):
    activity_type: str
    duration_minutes: float
    distance_km: float | None = None
    calories: float | None = None
    avg_heart_rate: int | None = None


class HealthEventOut(BaseModel):
    id: str
    user_id: str
    event_type: str
    activity_type: str | None
    duration_minutes: float | None
    timestamp: datetime

    model_config = {"from_attributes": True}


class MoodCreate(BaseModel):
    mood: int  # 1-5


class MoodOut(BaseModel):
    id: str
    mood: int
    timestamp: datetime

    model_config = {"from_attributes": True}


class CalendarEventOut(BaseModel):
    id: str
    title: str
    event_date: datetime
    notes: str | None

    model_config = {"from_attributes": True}


class GuidanceOverview(BaseModel):
    """All guidance for a user, grouped by voice."""

    class VoiceGuidance(BaseModel):
        voice: VoiceOut
        guidelines: list[GuidelineOut]

    voices: list[VoiceGuidance]
    platform_defaults: list[str]
