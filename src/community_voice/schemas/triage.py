"""The contract for what the Triage Agent must return."""

from enum import StrEnum

from pydantic import BaseModel, Field


class Language(StrEnum):
    ENGLISH = "en"
    ZULU = "zu"
    XHOSA = "xh"
    AFRIKAANS = "af"
    SESOTHO = "st"
    OTHER = "other"


class Category(StrEnum):
    WATER = "water"
    ELECTRICITY = "electricity"
    ROADS = "roads"
    SANITATION = "sanitation"
    WASTE = "waste"
    OTHER = "other"


class Urgency(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TriageResult(BaseModel):
    """Triage decision for one citizen report."""

    language: Language = Field(description="Language the report was written in.")
    english_text: str = Field(
        description="The report translated into English. If it is already in "
        "English, repeat it unchanged."
    )
    category: Category = Field(description="Which municipal service is affected.")
    summary: str = Field(description="One short English sentence summarising it.")
    urgency: Urgency = Field(description="How urgently this needs attention.")
    urgency_reason: str = Field(
        description="One short sentence explaining why this urgency was chosen."
    )
    area_mentioned: str | None = Field(
        default=None,
        description="Suburb, township or town named in the report, if any. "
        "Never include names of people, phone numbers or ID numbers.",
    )
