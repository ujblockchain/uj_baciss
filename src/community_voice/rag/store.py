"""Index and search the policy documents with Chroma (local embeddings)."""

import re

import chromadb

from community_voice.core.config import PROJECT_ROOT

POLICY_DIR = PROJECT_ROOT / "data" / "knowledge_base" / "policies"
INDEX_DIR = PROJECT_ROOT / "data" / "chroma"
COLLECTION = "policies"


def chunk_markdown(text: str, source: str) -> list[dict]:
    """Split a document into one chunk per '## ' section."""
    preamble, *sections = re.split(r"^## ", text, flags=re.MULTILINE)
    title = preamble.splitlines()[0].lstrip("# ").strip()
    chunks = []
    for number, section in enumerate(sections):
        heading, _, body = section.partition("\n")
        chunks.append(
            {
                "id": f"{source}-{number}",
                "text": f"{title}: {heading.strip()}\n{body.strip()}",
                "source": source,
            }
        )
    return chunks


def _collection() -> chromadb.Collection:
    client = chromadb.PersistentClient(path=str(INDEX_DIR))
    return client.get_or_create_collection(COLLECTION)


def build_index() -> int:
    """Rebuild the index from the policy files. Returns the number of chunks."""
    collection = _collection()
    old_ids = collection.get()["ids"]
    if old_ids:
        collection.delete(ids=old_ids)
    chunks = [
        chunk
        for path in sorted(POLICY_DIR.glob("*.md"))
        for chunk in chunk_markdown(path.read_text(encoding="utf-8"), path.name)
    ]
    collection.add(
        ids=[c["id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        metadatas=[{"source": c["source"]} for c in chunks],
    )
    return len(chunks)


def search(query: str, n_results: int = 3) -> list[dict]:
    """Return the chunks closest in meaning to the query (smaller distance = closer)."""
    collection = _collection()
    if collection.count() == 0:
        build_index()
    result = collection.query(query_texts=[query], n_results=n_results)
    return [
        {"text": text, "source": meta["source"], "distance": distance}
        for text, meta, distance in zip(
            result["documents"][0],
            result["metadatas"][0],
            result["distances"][0],
            strict=True,
        )
    ]
