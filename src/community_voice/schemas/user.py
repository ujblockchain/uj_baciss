"""Accounts: who is signed in, and what they may do."""

from typing import Literal

from pydantic import BaseModel

Role = Literal["citizen", "admin"]


class User(BaseModel):
    id: int
    email: str
    name: str
    role: Role


class StoredUser(User):
    """A user as saved: never sent to a client."""

    password_hash: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
