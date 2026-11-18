"""Web search tool for the Context Check Agent (Tavily)."""

from functools import lru_cache

from langchain.tools import tool
from langchain_tavily import TavilySearch

from community_voice.core.config import get_settings

# Kept small: the model's free tier allows only about 8,000 tokens per request.
MAX_RESULTS = 3
SNIPPET_CHARS = 200


@lru_cache
def _tavily() -> TavilySearch:
    return TavilySearch(
        max_results=MAX_RESULTS,
        time_range="month",
        # The library calls str() on the key, which would give "**********".
        tavily_api_key=get_settings().tavily_api_key.get_secret_value(),
    )


def format_results(result) -> str:
    """Turn a Tavily response into short text: title, URL and a snippet."""
    if isinstance(result, dict) and "error" in result:
        return f"Search error: {result['error']}"
    if not isinstance(result, dict) or not result.get("results"):
        return "No results found."
    blocks = []
    for item in result["results"]:
        snippet = " ".join(item["content"].split())[:SNIPPET_CHARS]
        blocks.append(f"{item['title']}\n{item['url']}\n{snippet}")
    return "\n\n".join(blocks)


@tool
def web_search(query: str) -> str:
    """Search the web for news and notices from the last month.

    Use short keywords: the service, the area and the municipality.
    """
    return format_results(_tavily().invoke({"query": query}))
