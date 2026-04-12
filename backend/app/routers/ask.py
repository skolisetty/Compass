"""Main question endpoint: the heart of Compass."""

import logging
import traceback

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import AskRequest, AskResponse
from app.services.llm_provider import ask_llm
from app.services.prompt_builder import build_system_prompt

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["ask"])


@router.post("/ask", response_model=AskResponse)
async def ask(body: AskRequest, db: Session = Depends(get_db)):
    try:
        system_prompt, guideline_records = build_system_prompt(db, body.user_id)
        answer, attributions = await ask_llm(system_prompt, body.question, guideline_records)
        return AskResponse(answer=answer, attributions=attributions)
    except Exception as e:
        logger.error(f"Ask endpoint error: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
