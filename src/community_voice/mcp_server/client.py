"""How agents reach the MCP server. This is the only place that knows the transport."""

from langchain_mcp_adapters.client import MultiServerMCPClient

from community_voice.mcp_server import HOST, PORT


def mcp_connections() -> dict:
    """HTTP: connect to a server that is already running."""
    return {
        "directory": {
            "transport": "http",
            "url": f"http://{HOST}:{PORT}/mcp",
        }
    }


async def get_mcp_tools() -> list:
    """Load the server's tools as LangChain tools."""
    return await MultiServerMCPClient(mcp_connections()).get_tools()
