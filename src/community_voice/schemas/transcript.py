"""What speech-to-text returns."""

from pydantic import BaseModel


class Transcript(BaseModel):
    text: str
    warning: str  # always shown: the citizen must check the text
