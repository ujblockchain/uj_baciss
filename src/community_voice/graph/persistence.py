"""The checkpointer: saves the graph's state to SQLite after every step."""

import sqlite3
from pathlib import Path

from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langgraph.checkpoint.sqlite import SqliteSaver

from community_voice.core.config import CHECKPOINT_PATH
from community_voice.schemas.context_check import (
    Confidence,
    ContextCheckResult,
    Finding,
    Source,
)
from community_voice.schemas.draft import DraftDecision, DraftResponse
from community_voice.schemas.duplicate import DuplicateResult
from community_voice.schemas.report import ReportIn
from community_voice.schemas.review import ReviewDecision
from community_voice.schemas.routing import RoutingResult
from community_voice.schemas.triage import Category, Language, TriageResult, Urgency

# Our types that appear in the graph state. Only these (plus LangGraph's own safe
# types) may be loaded back from a checkpoint.
STATE_TYPES = [
    ReportIn,
    Language,
    Category,
    Urgency,
    TriageResult,
    RoutingResult,
    Finding,
    Confidence,
    Source,
    ContextCheckResult,
    DuplicateResult,
    ReviewDecision,
    DraftResponse,
    DraftDecision,
]


def get_checkpointer(path: Path = CHECKPOINT_PATH) -> SqliteSaver:
    path.parent.mkdir(parents=True, exist_ok=True)
    serde = JsonPlusSerializer(allowed_msgpack_modules=STATE_TYPES)
    return SqliteSaver(sqlite3.connect(path, check_same_thread=False), serde=serde)
