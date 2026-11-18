"""Model-provider layer: one place that decides which LLM an agent talks to."""

from typing import Literal

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from community_voice.core.config import get_settings

Provider = Literal["gemini", "groq"]


def get_chat_model(provider: Provider) -> BaseChatModel:
    """Return a chat model for the given provider, configured from settings."""
    settings = get_settings()

    if provider == "gemini":
        return ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            api_key=settings.gemini_api_key,
            max_retries=2,
        )
    if provider == "groq":
        return ChatGroq(
            model=settings.groq_model,
            api_key=settings.groq_api_key,
            max_retries=2,
        )
    raise ValueError(f"Unknown provider: {provider!r}")
