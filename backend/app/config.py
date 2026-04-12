from pathlib import Path

from pydantic_settings import BaseSettings

_env_path = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    openai_api_key: str = ""
    llm_model: str = "gpt-4o-mini"
    database_url: str = "sqlite:///./compass.db"

    model_config = {"env_file": str(_env_path), "env_file_encoding": "utf-8"}


settings = Settings()
