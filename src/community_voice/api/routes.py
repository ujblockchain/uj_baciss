"""The API endpoints."""

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.sse import EventSourceResponse, ServerSentEvent
from langgraph.types import Command

from community_voice.api.dependencies import (
    AdminUser,
    CurrentUser,
    GraphDep,
    TranscriberDep,
    can_see,
    read_limited,
    require_waiting,
)
from community_voice.api.schemas import (
    STAGES,
    DraftOutcome,
    MyReport,
    PhotoOutcome,
    ReportDetail,
    SampleOut,
    StartedEvent,
)
from community_voice.api.stats import Stats, build_stats
from community_voice.api.streaming import WAITING, stream_run, thread_config
from community_voice.core.config import SAMPLES_PATH
from community_voice.db.repository import (
    get_draft,
    get_report,
    list_pending,
    list_reports,
    list_reports_of,
    set_owner,
)
from community_voice.media.photos import (
    MAX_PHOTO_BYTES,
    InvalidPhoto,
    photo_path,
    save_photo,
)
from community_voice.media.transcribe import (
    AUDIO_TYPES,
    MAX_AUDIO_BYTES,
    TranscriptionError,
)
from community_voice.schemas.draft import DraftDecision
from community_voice.schemas.report import ReportIn
from community_voice.schemas.review import ReportRecord, ReviewDecision
from community_voice.schemas.transcript import Transcript

router = APIRouter()

WaitingForReview = Annotated[str, Depends(require_waiting("human_review"))]
WaitingForDraft = Annotated[str, Depends(require_waiting("draft_review"))]


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/transcriptions")
def transcribe_voice_note(
    audio: UploadFile, transcriber: TranscriberDep, user: CurrentUser
) -> Transcript:
    """Turn a voice note into text. The citizen checks it, then submits a report."""
    extension = Path(audio.filename or "").suffix.lstrip(".").lower()
    if extension not in AUDIO_TYPES:
        raise HTTPException(status_code=415, detail="Unsupported audio format.")
    data = read_limited(audio, MAX_AUDIO_BYTES, "recording")
    try:
        transcript = transcriber(data, audio.filename)
    except TranscriptionError:
        raise HTTPException(status_code=502, detail="Transcription failed.") from None
    if not transcript.text:
        raise HTTPException(status_code=422, detail="No speech was found.")
    return transcript


@router.post("/reports", response_class=EventSourceResponse)
def submit_report(
    report: ReportIn, graph: GraphDep, user: CurrentUser
) -> Iterator[ServerSentEvent]:
    """Run a new report through the workflow, streaming each step."""
    report_id = f"r-{uuid4().hex[:8]}"
    set_owner(report_id, user.id)
    yield ServerSentEvent(data=StartedEvent(report_id=report_id), event="started")
    graph_input = {"report_id": report_id, "report": report}
    yield from stream_run(graph, graph_input, report_id, user.role == "admin")


@router.get("/reviews")
def review_queue(admin: AdminUser) -> list[ReportRecord]:
    """Reports waiting for a reviewer, most urgent first."""
    return list_pending()


@router.get("/stats")
def stats(admin: AdminUser) -> Stats:
    return build_stats(list_reports())


@router.get("/samples")
def samples(user: CurrentUser) -> list[SampleOut]:
    """Sample reports for demos."""
    items = json.loads(SAMPLES_PATH.read_text(encoding="utf-8"))
    return [SampleOut(**{k: item[k] for k in SampleOut.model_fields}) for item in items]


@router.get("/my/reports")
def my_reports(user: CurrentUser) -> list[MyReport]:
    """The signed-in person's own reports."""
    return [_my_report(record) for record in list_reports_of(user.id)]


def _my_report(record: ReportRecord) -> MyReport:
    draft = get_draft(record.id)
    approved = record.status == "ready_to_send" and draft
    return MyReport(
        id=record.id,
        text=record.text,
        status=record.status,
        stage=STAGES.get(record.status, "In progress"),
        reply=draft["body"] if approved else None,
        created_at=record.created_at,
        has_photo=photo_path(record.id).exists(),
    )


@router.get("/reports/{report_id}")
def read_report(report_id: str, graph: GraphDep, admin: AdminUser) -> ReportDetail:
    record = get_report(report_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Report not found.")
    snapshot = graph.get_state(thread_config(report_id))
    draft = get_draft(report_id)
    return ReportDetail(
        report=record,
        waiting_for=WAITING[snapshot.next[0]] if snapshot.next else None,
        pending=snapshot.interrupts[0].value if snapshot.interrupts else None,
        draft=draft["body"] if draft else None,
        has_photo=photo_path(report_id).exists(),
    )


@router.put("/reports/{report_id}/photo")
def attach_photo(report_id: str, photo: UploadFile, user: CurrentUser) -> PhotoOutcome:
    """Attach an optional photo for the human reviewer."""
    if get_report(report_id) is None or not can_see(report_id, user):
        raise HTTPException(status_code=404, detail="Report not found.")
    data = read_limited(photo, MAX_PHOTO_BYTES, "photo")
    try:
        size = save_photo(report_id, data)
    except InvalidPhoto as error:
        raise HTTPException(status_code=415, detail=str(error)) from None
    return PhotoOutcome(report_id=report_id, size=size)


@router.get("/reports/{report_id}/photo")
def read_photo(report_id: str, user: CurrentUser) -> FileResponse:
    path = photo_path(report_id)
    if (
        get_report(report_id) is None
        or not can_see(report_id, user)
        or not path.exists()
    ):
        raise HTTPException(status_code=404, detail="No photo for this report.")
    return FileResponse(path, media_type="image/jpeg")


@router.post("/reports/{report_id}/review", response_class=EventSourceResponse)
def review_report(
    report_id: WaitingForReview, decision: ReviewDecision, graph: GraphDep
) -> Iterator[ServerSentEvent]:
    """Send the reviewer's decision and stream the steps that follow."""
    command = Command(resume=decision.model_dump(mode="json"))
    yield from stream_run(graph, command, report_id)


@router.post("/reports/{report_id}/draft")
def decide_draft(
    report_id: WaitingForDraft, decision: DraftDecision, graph: GraphDep
) -> DraftOutcome:
    """Send the reviewer's decision on the drafted reply."""
    command = Command(resume=decision.model_dump(mode="json"))
    result = graph.invoke(command, thread_config(report_id), version="v2")
    return DraftOutcome(
        report_id=report_id,
        status=result.value["status"],
        draft=result.value["draft"].body,
    )
