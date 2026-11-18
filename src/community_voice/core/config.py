"""Application settings, loaded from environment variables and the .env file."""

from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# core/config.py -> core -> community_voice -> src -> project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_PATH = PROJECT_ROOT / "data" / "app.db"  # reports and reviews
CHECKPOINT_PATH = PROJECT_ROOT / "data" / "checkpoints.db"  # saved graph state
MEMORY_PATH = PROJECT_ROOT / "data" / "memory.db"  # long-term memory
PHOTO_DIR = PROJECT_ROOT / "data" / "uploads" / "photos"  # report photos
SAMPLES_PATH = PROJECT_ROOT / "data" / "sample_reports" / "reports.json"


class Settings(BaseSettings):
    """Typed settings. Keys are SecretStr so they never print by accident."""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",  # .env also holds keys we do not use yet (LangSmith)
    )

    gemini_api_key: SecretStr
    groq_api_key: SecretStr
    tavily_api_key: SecretStr
    jwt_secret: SecretStr | None = None  # signs login tokens (accounts)

    gemini_model: str = "gemini-3.1-flash-lite"
    groq_model: str = "openai/gpt-oss-20b"


@lru_cache
def get_settings() -> Settings:
    """Load settings once and reuse them."""
    return Settings()
