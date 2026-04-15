"""Compass -- Your AI, guided by the Voices who know you."""

import logging
import os
from contextlib import asynccontextmanager
from logging.handlers import RotatingFileHandler
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, SessionLocal, engine
from app.routers import ask, context, guidelines
from app.seed_data import seed

_LOG_PATH = Path(__file__).resolve().parent.parent / "logs" / "compass.log"


def _configure_file_logging() -> None:
    """Append a rotating file handler to the root logger (keeps Uvicorn's console handlers)."""
    _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger()
    target = os.path.normcase(os.path.abspath(_LOG_PATH))
    for h in root.handlers:
        if isinstance(h, RotatingFileHandler):
            if os.path.normcase(os.path.abspath(h.baseFilename)) == target:
                return
    fmt = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
    fh = RotatingFileHandler(
        _LOG_PATH, maxBytes=1_048_576, backupCount=5, encoding="utf-8"
    )
    fh.setLevel(logging.INFO)
    fh.setFormatter(fmt)
    root.addHandler(fh)


_configure_file_logging()

logger = logging.getLogger(__name__)
logger.info("File log: %s", _LOG_PATH)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    if not settings.openai_api_key.strip():
        logger.warning(
            "OPENAI_API_KEY is empty or missing; /api/ask will fail until it is set in .env"
        )
    else:
        logger.info(f"OPENAI_API_KEY is set to {settings.openai_api_key}")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()
    yield


app = FastAPI(title="Compass", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(guidelines.router)
app.include_router(ask.router)
app.include_router(context.router)


@app.get("/api/health-check")
def health_check():
    return {"status": "ok", "product": "Compass"}
