"""Sign in and who am I."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from community_voice.api.dependencies import CurrentUser
from community_voice.auth.security import check_password, create_token
from community_voice.db.repository import find_user
from community_voice.schemas.user import Token, User

router = APIRouter()


@router.post("/auth/login")
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """Exchange an email (sent as "username") and password for a token."""
    user = find_user(form.username)
    if not check_password(form.password, user.password_hash if user else None):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=create_token(user.id))


@router.get("/me")
def me(user: CurrentUser) -> User:
    return user
