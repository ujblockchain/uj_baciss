"""Input models: a citizen report, and a labelled sample report for testing."""

from pydantic import BaseModel, Field

from community_voice.schemas.triage import Category, Language, Urgency


class ReportIn(BaseModel):
    """A citizen report as it enters the system."""

    text: str = Field(min_length=5, max_length=2000)


class SampleReport(BaseModel):
    """A fictional report with the answer we expect, used to check the agent."""

    id: str
    language: Language
    text: str
    expected_category: Category
    expected_urgency: Urgency
