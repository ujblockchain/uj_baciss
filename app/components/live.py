"""Show a streamed run as it happens."""

import httpx
import streamlit as st

from components import api


def watch(path: str, payload: dict, label: str) -> tuple[str | None, str]:
    """Stream a run into a status box. Returns (report id, last event name)."""
    report_id, last, trace = None, "error", []
    with st.status(label, expanded=True) as box:
        try:
            for name, data in api.stream(path, payload):
                last = name
                if name == "started":
                    report_id = data["report_id"]
                elif name == "step":
                    line = f"{data['node']}: {data['message']}"
                    trace.append(line)
                    st.write(line)
                elif name == "error":
                    st.error(data["message"])
        except httpx.HTTPError as error:
            st.error(api.explain(error))
        box.update(label=label, state="error" if last == "error" else "complete")
    st.session_state["trace"] = trace
    return report_id, last
