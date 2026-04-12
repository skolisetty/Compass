"""Compass -- Your AI, guided by the Voices who know you."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, SessionLocal, engine
from app.routers import ask, context, guidelines
from app.seed_data import seed


@asynccontextmanager
async def lifespan(_app: FastAPI):
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
