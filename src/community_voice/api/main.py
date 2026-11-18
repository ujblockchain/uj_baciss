"""The FastAPI app. Run: uv run uvicorn community_voice.api.main:app --port 8800"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from community_voice.api.auth_routes import router as auth_router
from community_voice.api.routes import router
from community_voice.core.tracing import load_env
from community_voice.graph.memory import get_store
from community_voice.graph.persistence import get_checkpointer
from community_voice.graph.workflow import build_graph


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Build the workflow once, when the server starts."""
    load_env()  # lets LangSmith tracing read .env
    app.state.graph = build_graph(get_checkpointer(), get_store())
    yield


# Browsers only let the Next.js app (these origins) call the API. The token travels
# in the Authorization header, so cookies (credentials) are not needed.
FRONTEND_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000", "https://p01--community-voice-frontend--hrjmz5y4vxfz.code.run"]

app = FastAPI(title="Community Voice API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["Authorization", "Content-Type"],
)
app.include_router(auth_router)
app.include_router(router)
