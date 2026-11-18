"""Passwords and login tokens, as in the FastAPI security tutorial."""

from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from community_voice.core.config import get_settings

ALGORITHM = "HS256"
TOKEN_MINUTES = 30

_hasher = PasswordHash.recommended()
# Checked when the email is unknown, so timing does not reveal which emails exist.
_DUMMY_HASH = _hasher.hash("not-a-real-password")


def get_jwt_secret() -> str:
    secret = get_settings().jwt_secret
    if secret is None:
        raise RuntimeError("Set JWT_SECRET in .env (see the README).")
    return secret.get_secret_value()


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def check_password(password: str, stored_hash: str | None) -> bool:
    """False for an unknown user, after the same work as for a real one."""
    matches = _hasher.verify(password, stored_hash or _DUMMY_HASH)
    return matches and stored_hash is not None


def create_token(user_id: int, minutes: int = TOKEN_MINUTES) -> str:
    expires = datetime.now(UTC) + timedelta(minutes=minutes)
    claims = {"sub": str(user_id), "exp": expires}
    return jwt.encode(claims, get_jwt_secret(), algorithm=ALGORITHM)


def read_token(token: str) -> int | None:
    """The user id inside a valid, unexpired token, otherwise None."""
    try:
        claims = jwt.decode(token, get_jwt_secret(), algorithms=[ALGORITHM])
        return int(claims["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        return None
