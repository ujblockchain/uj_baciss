"""Models for what the API sends back."""

from typing import Any

from pydantic import BaseModel

from community_voice.schemas.review import ReportRecord


class StartedEvent(BaseModel):
    report_id: str


class StepEvent(BaseModel):
    node: str
    message: str


class PausedEvent(BaseModel):
    waiting_for: str  # "review" or "draft"
    payload: Any  # what the reviewer needs to see


class DoneEvent(BaseModel):
    status: str


class ErrorEvent(BaseModel):
    message: str


class ReportDetail(BaseModel):
    report: ReportRecord
    waiting_for: str | None = None
    pending: Any = None
    draft: str | None = None
    has_photo: bool = False


# What a citizen is told, whatever the internal status is.
STAGES = {
    "ready_for_review": "Received, waiting for review",
    "fast_track": "Received, waiting for review",
    "duplicate": "Received, waiting for review",
    "needs_human": "Received, waiting for review",
    "approved": "Reviewed, reply being prepared",
    "draft_rejected": "Reviewed. A reply will follow",
    "ready_to_send": "Resolved: see the reply",
    "known_planned_outage": "Known planned outage in your area",
    "rejected": "Closed",
}


class MyReport(BaseModel):
    """What a citizen sees of their own report."""

    id: str
    text: str
    status: str
    stage: str  # the status in plain words
    reply: str | None  # the approved reply, once there is one
    created_at: str
    has_photo: bool


class PhotoOutcome(BaseModel):
    report_id: str
    size: int  # bytes stored


class SampleOut(BaseModel):
    id: str
    language: str
    text: str


class DraftOutcome(BaseModel):
    report_id: str
    status: str
    draft: str
