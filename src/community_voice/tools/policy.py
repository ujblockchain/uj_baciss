"""Tool that lets an agent search the policy documents."""

from langchain.tools import tool

from community_voice.rag.store import search


@tool
def search_policy(query: str) -> str:
    """Search service charters, response-time rules and reply templates.

    Use for questions about response times, procedures and wording.
    """
    hits = search(query)
    return "\n\n".join(f"[{hit['source']}]\n{hit['text']}" for hit in hits)
