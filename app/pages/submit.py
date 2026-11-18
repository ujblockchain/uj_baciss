"""Page 1: a citizen submits a report by text, voice note and photo."""

import httpx
import streamlit as st
from components import api, live

st.title("Submit a report")

# Sample picker (demo only): fills the text box.
try:
    samples = {s["id"]: s for s in api.get("/samples")}
except httpx.HTTPError as error:
    st.error(api.explain(error))
    st.stop()


def use_sample() -> None:
    sample = samples.get(st.session_state.sample)
    if sample:
        st.session_state.text = sample["text"]


def sample_label(sample_id: str) -> str:
    if not sample_id:
        return "None"
    sample = samples[sample_id]
    return f"{sample['language']}: {sample['text'][:60]}"


st.selectbox(
    "Sample report (demo)",
    ["", *samples],
    format_func=sample_label,
    key="sample",
    on_change=use_sample,
)

# Voice note: transcribe, then the citizen checks the text below.
audio = st.audio_input("Voice note (optional)") or st.file_uploader(
    "or upload a recording", type=["mp3", "m4a", "wav", "ogg", "flac", "webm"]
)
if audio and st.button("Transcribe"):
    try:
        voice = api.send(
            "POST", "/transcriptions", files={"audio": (audio.name, audio.getvalue())}
        )
        st.session_state.text = voice["text"]
        st.warning(voice["warning"])
    except httpx.HTTPError as error:
        st.error(api.explain(error))

text = st.text_area("Report", key="text", height=160)
photo = st.file_uploader(
    "Photo (optional, max 5 MB)", type=["jpg", "jpeg", "jfif", "png", "webp"]
)

if st.button("Submit report", type="primary"):
    if len(text.strip()) < 5:
        st.warning("Please describe the problem (at least 5 characters).")
        st.stop()
    report_id, last = live.watch("/reports", {"text": text}, "Agents working")
    if report_id and photo and last in ("paused", "done"):
        try:
            api.send(
                "PUT",
                f"/reports/{report_id}/photo",
                files={"photo": (photo.name, photo.getvalue())},
            )
        except httpx.HTTPError as error:
            st.warning(f"Photo not saved: {api.explain(error)}")
    if last == "paused":
        st.success(f"Report {report_id} is waiting for a reviewer.")
    elif last == "done":
        st.success(f"Report {report_id} is finished without review.")
