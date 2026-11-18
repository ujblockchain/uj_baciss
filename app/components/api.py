"""A small client for the Community Voice API."""

import json
from collections.abc import Iterator
from typing import Any

import httpx
import streamlit as st

BASE = "http://127.0.0.1:8800"


def _headers() -> dict:
    """The signed-in user's token, sent with every request."""
    token = st.session_state.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}


def login(email: str, password: str) -> None:
    """Sign in and keep the token for this browser session."""
    response = httpx.post(
        BASE + "/auth/login", data={"username": email, "password": password}
    )
    response.raise_for_status()
    st.session_state["token"] = response.json()["access_token"]


def get(path: str) -> Any:
    response = httpx.get(BASE + path, headers=_headers(), timeout=30)
    response.raise_for_status()
    return response.json()


def get_bytes(path: str) -> bytes:
    response = httpx.get(BASE + path, headers=_headers(), timeout=30)
    response.raise_for_status()
    return response.content


def send(method: str, path: str, **kwargs: Any) -> Any:
    """A JSON or file-upload request that answers with JSON."""
    response = httpx.request(
        method, BASE + path, headers=_headers(), timeout=120, **kwargs
    )
    response.raise_for_status()
    return response.json()


def stream(path: str, payload: dict) -> Iterator[tuple[str, dict]]:
    """POST and yield (event, data) as each server-sent event arrives."""
    name = ""
    with httpx.stream(
        "POST", BASE + path, json=payload, headers=_headers(), timeout=180
    ) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if line.startswith("event:"):
                name = line.split(":", 1)[1].strip()
            elif line.startswith("data:"):
                yield name, json.loads(line.split(":", 1)[1])


def explain(error: httpx.HTTPError) -> str:
    """A short message for the screen."""
    if isinstance(error, httpx.HTTPStatusError):
        if error.response.status_code == 401 and "token" in st.session_state:
            del st.session_state["token"]
            return "Your session ended. Please sign in again."
        try:
            return str(error.response.json()["detail"])
        except (ValueError, KeyError):
            return f"The API answered {error.response.status_code}."
    return "Cannot reach the API. Is it running on port 8800?"
