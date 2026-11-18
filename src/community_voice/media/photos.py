"""Photo checks and storage. Photos are for the human reviewer only."""

from io import BytesIO

from PIL import Image, ImageOps, UnidentifiedImageError

from community_voice.core.config import PHOTO_DIR

MAX_PHOTO_BYTES = 5 * 1024 * 1024
MAX_PIXELS = 40_000_000
MAX_SIDE = 1600
FORMATS = ["JPEG", "PNG", "WEBP"]


class InvalidPhoto(ValueError):
    """The upload is not a usable photo."""


def clean_photo(data: bytes) -> bytes:
    """Check the image by decoding it, then return a small JPEG without metadata."""
    try:
        with Image.open(BytesIO(data), formats=FORMATS) as image:
            if image.width * image.height > MAX_PIXELS:
                raise InvalidPhoto("The photo has too many pixels.")
            image.load()
            photo = ImageOps.exif_transpose(image).convert("RGB")
    except (UnidentifiedImageError, Image.DecompressionBombError, OSError) as error:
        raise InvalidPhoto("The file is not a JPEG, PNG or WebP photo.") from error
    photo.thumbnail((MAX_SIDE, MAX_SIDE))
    out = BytesIO()
    photo.save(out, "JPEG", quality=85)  # no exif argument: location is dropped
    return out.getvalue()


def photo_path(report_id: str):
    return PHOTO_DIR / f"{report_id}.jpg"


def save_photo(report_id: str, data: bytes) -> int:
    """Clean and store the photo. Returns the stored size in bytes."""
    cleaned = clean_photo(data)
    PHOTO_DIR.mkdir(parents=True, exist_ok=True)
    photo_path(report_id).write_bytes(cleaned)
    return len(cleaned)
