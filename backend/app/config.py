import os
import subprocess
from pathlib import Path

from pydantic_settings import BaseSettings

_env_path = Path(__file__).resolve().parent.parent / ".env"


def _resolve_env_var(name: str) -> str:
    """Read from process env first, then fall back to the Windows user/system
    environment (which Cursor terminals don't always inherit)."""
    val = os.environ.get(name, "")
    if val:
        return val
    try:
        result = subprocess.run(
            ["powershell", "-Command",
             f"[System.Environment]::GetEnvironmentVariable('{name}', 'User')"],
            capture_output=True, text=True, timeout=5,
        )
        val = result.stdout.strip()
    except Exception:
        pass
    return val


class Settings(BaseSettings):
    openai_api_key: str = ""
    llm_model: str = "gpt-4o-mini"
    database_url: str = "sqlite:///./compass.db"

    model_config = {"env_file": str(_env_path), "env_file_encoding": "utf-8"}


settings = Settings()

if not settings.openai_api_key:
    settings.openai_api_key = _resolve_env_var("OPENAI_API_KEY")
