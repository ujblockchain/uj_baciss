"""Long-term memory: reviewer corrections, reused as hints for triage."""

import sqlite3
from functools import lru_cache
from pathlib import Path

from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from langgraph.store.base import BaseStore
from langgraph.store.sqlite import SqliteStore

from community_voice.core.config import MEMORY_PATH
from community_voice.schemas.review import ReviewDecision
from community_voice.schemas.triage import TriageResult

NAMESPACE = ("corrections",)
DIMS = 384  # size of the local embedding model's vectors
# Ignore weak matches. Similar reports scored 0.36 to 0.4, an unrelated one 0.06.
MIN_SCORE = 0.2


@lru_cache
def _embedder() -> DefaultEmbeddingFunction:
    return DefaultEmbeddingFunction()


def _embed(texts) -> list[list[float]]:
    return [[float(x) for x in vector] for vector in _embedder()(list(texts))]


def get_store(path: Path = MEMORY_PATH) -> SqliteStore:
    """A persistent store that can search by meaning, using the local model."""
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, check_same_thread=False, isolation_level=None)
    index = {"embed": _embed, "dims": DIMS, "fields": ["text"]}
    store = SqliteStore(connection, index=index)
    store.setup()
    return store


def remember_correction(
    store: BaseStore | None,
    report_id: str,
    text: str,
    triaged: TriageResult,
    department: str,
    decision: ReviewDecision,
) -> bool:
    """Save a reviewer's change of category, urgency or department. True if saved."""
    if store is None or decision.action != "approve":
        return False
    ai = {
        "category": triaged.category.value,
        "urgency": triaged.urgency.value,
        "department": department,
    }
    chosen = {
        "category": decision.category.value if decision.category else None,
        "urgency": decision.urgency.value if decision.urgency else None,
        "department": decision.department,
    }
    changes = {
        name: value for name, value in chosen.items() if value and value != ai[name]
    }
    if not changes:
        return False
    store.put(
        NAMESPACE,
        report_id,
        {
            "text": text,
            "summary": triaged.summary,
            "ai": ai,
            "corrected": changes,
            "note": decision.note,
        },
    )
    return True


def _hint(value: dict) -> str:
    changes = ", ".join(
        f"{name} from {value['ai'][name]} to {new}"
        for name, new in value["corrected"].items()
    )
    note = f" Note: {value['note']}" if value["note"] else ""
    return f"Similar report ({value['summary']}): a reviewer changed {changes}.{note}"


def find_hints(
    store: BaseStore | None, text: str, limit: int = 3, min_score: float = MIN_SCORE
) -> list[str]:
    """Past corrections for reports similar to this text, as short sentences."""
    if store is None:
        return []
    items = store.search(NAMESPACE, query=text, limit=limit)
    return [_hint(i.value) for i in items if i.score is None or i.score >= min_score]


def reset_memory(store: BaseStore) -> None:
    """Delete all remembered corrections."""
    for item in store.search(NAMESPACE, limit=1000):
        store.delete(NAMESPACE, item.key)
