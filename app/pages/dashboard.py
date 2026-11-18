"""Page 3: counts, urgent items, duplicates and the last agent trace."""

import httpx
import pandas as pd
import streamlit as st
from components import api

st.title("Dashboard")

try:
    stats = api.get("/stats")
except httpx.HTTPError as error:
    st.error(api.explain(error))
    st.stop()

st.metric("Reports", stats["total"])
if stats["total"]:
    for title, key in [
        ("By status", "by_status"),
        ("By category", "by_category"),
        ("By department", "by_department"),
        ("By urgency", "by_urgency"),
    ]:
        st.subheader(title)
        st.bar_chart(pd.Series(stats[key]))

st.subheader("Urgent, still waiting")
if stats["urgent"]:
    columns = ["id", "urgency", "category", "department", "status"]
    st.dataframe(pd.DataFrame(stats["urgent"])[columns], hide_index=True)
else:
    st.write("None.")

st.subheader("Duplicate clusters")
for original, duplicates in stats["duplicate_clusters"].items():
    st.write(f"{original} is repeated by {', '.join(duplicates)}")
if not stats["duplicate_clusters"]:
    st.write("None.")

with st.expander("Agent Trace (steps of your last run)"):
    for line in st.session_state.get("trace") or ["No run yet in this session."]:
        st.write(line)
