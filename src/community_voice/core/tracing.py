"""Tracing is switched on in .env (LANGSMITH_TRACING=true).

LangChain reads real environment variables only, so we load .env into them.
Variables that are already set win.
"""

from dotenv import load_dotenv

from community_voice.core.config import PROJECT_ROOT


def load_env() -> None:
    load_dotenv(PROJECT_ROOT / ".env")
