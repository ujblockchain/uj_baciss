"""Speech-to-text with Gemini."""

import base64
import logging

from google import genai

from community_voice.core.config import get_settings
from community_voice.schemas.transcript import Transcript

logger = logging.getLogger(__name__)

MODEL = "gemini-3.5-transcribe"
MAX_AUDIO_BYTES = 10 * 1024 * 1024
MIME_TYPES = {
    "wav": "audio/wav",
    "mp3": "audio/mp3",
    "aiff": "audio/aiff",
    "aac": "audio/aac",
    "ogg": "audio/ogg",
    "flac": "audio/flac",
    "mpeg": "audio/mpeg",
    "m4a": "audio/m4a",
    "opus": "audio/opus",
    "webm": "audio/webm",
}
AUDIO_TYPES = set(MIME_TYPES)
WARNING = (
    "Automatic transcription. Please check the text. "
    "isiZulu, isiXhosa, Sesotho and Setswana are experimental."
)


class TranscriptionError(Exception):
    """The speech service failed."""


def get_client() -> genai.Client:
    return genai.Client(
        api_key=get_settings().gemini_api_key.get_secret_value(),
        http_options={"api_version": "v1beta"},
    )


def transcribe(
    audio: bytes, filename: str, client: genai.Client | None = None
) -> Transcript:
    """Turn a voice note into text. The citizen always checks it."""
    extension = filename.rsplit(".", 1)[-1].lower()
    content = {
        "type": "audio",
        "data": base64.b64encode(audio).decode(),
        "mime_type": MIME_TYPES[extension],
    }
    try:
        client = client or get_client()
        response = client.interactions.create(model=MODEL, input=[content])
    except Exception as error:
        logger.exception("Transcription failed")
        raise TranscriptionError from error
    return Transcript(text=response.output_text.strip(), warning=WARNING)
