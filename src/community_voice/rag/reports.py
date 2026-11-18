"""Temporary store of processed reports in Chroma (replaced in Phase 7)."""

import chromadb

from community_voice.rag.store import INDEX_DIR

COLLECTION = "reports"


def _collection() -> chromadb.Collection:
    client = chromadb.PersistentClient(path=str(INDEX_DIR))
    return client.get_or_create_collection(COLLECTION)


def add_report(report_id: str, text: str, category: str) -> None:
    """Store a report so later reports can be compared with it."""
    _collection().upsert(
        ids=[report_id], documents=[text], metadatas=[{"category": category}]
    )


def find_similar(text: str, category: str, n_results: int = 3) -> list[dict]:
    """Return stored reports in the same category, closest first."""
    collection = _collection()
    if collection.count() == 0:
        return []
    result = collection.query(
        query_texts=[text], n_results=n_results, where={"category": category}
    )
    return [
        {"id": report_id, "text": document, "distance": distance}
        for report_id, document, distance in zip(
            result["ids"][0],
            result["documents"][0],
            result["distances"][0],
            strict=True,
        )
    ]


def reset_reports() -> None:
    """Delete all stored reports."""
    collection = _collection()
    ids = collection.get()["ids"]
    if ids:
        collection.delete(ids=ids)
