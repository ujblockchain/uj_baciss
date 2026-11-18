"""Shared pieces that endpoints ask for."""

from collections.abc import Callable
from typing import Annotated, Any

from fastapi import Depends, HTTPException, Request, UploadFile
from fastapi.security import OAuth2PasswordBearer

from community_voice.api.streaming import WAITING, thread_config
from community_voice.auth.security import read_token
from community_voice.db.repository import get_owner, get_report, get_user
from community_voice.media.transcribe import transcribe
from community_voice.schemas.transcript import Transcript
from community_voice.schemas.user import User


def get_graph(request: Request) -> Any:
    """The workflow, built once at startup."""
    return request.app.state.graph


GraphDep = Annotated[Any, Depends(get_graph)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """The signed-in user, or 401."""
    user_id = read_token(token)
    user = get_user(user_id) if user_id is not None else None
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_admin(user: CurrentUser) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only.")
    return user


AdminUser = Annotated[User, Depends(require_admin)]


def can_see(report_id: str, user: User) -> bool:
    """Admins see every report; a citizen sees only their own."""
    return user.role == "admin" or get_owner(report_id) == user.id


def get_transcriber() -> Callable[[bytes, str], Transcript]:
    """The speech-to-text function (tests swap it for a stub)."""
    return transcribe


TranscriberDep = Annotated[Callable[[bytes, str], Transcript], Depends(get_transcriber)]


def read_limited(upload: UploadFile, limit: int, what: str) -> bytes:
    """Read an upload, refusing anything over `limit` bytes with a 413."""
    data = upload.file.read(limit + 1)
    if len(data) > limit:
        detail = f"The {what} is too large (limit {limit // 1024 // 1024} MB)."
        raise HTTPException(status_code=413, detail=detail)
    return data


def require_waiting(node: str):
    """Check a report exists and is paused at `node`, before any work starts."""

    def check(report_id: str, graph: GraphDep, admin: AdminUser) -> str:
        if get_report(report_id) is None:
            raise HTTPException(status_code=404, detail="Report not found.")
        if graph.get_state(thread_config(report_id)).next != (node,):
            detail = f"This report is not waiting for a {WAITING[node]} decision."
            raise HTTPException(status_code=409, detail=detail)
        return report_id

    return check
