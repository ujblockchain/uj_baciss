"""Page: a person follows their own reports and reads the reply."""

import httpx
import streamlit as st
from components import api

st.title("My reports")

try:
    reports = api.get("/my/reports")
except httpx.HTTPError as error:
    st.error(api.explain(error))
    st.stop()

if not reports:
    st.info("You have not submitted a report yet.")
for report in reports:
    with st.container(border=True):
        st.caption(f"{report['id']} | {report['created_at']}")
        st.write(report["text"])
        st.write(f"**Status:** {report['stage']}")
        if report["reply"]:
            st.write("**Reply:**")
            st.write(report["reply"])
        if report["has_photo"]:
            st.image(api.get_bytes(f"/reports/{report['id']}/photo"), width=300)
