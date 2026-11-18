"""Page 2: a reviewer checks reports, then the drafted reply."""

import httpx
import streamlit as st
from components import api, live

from community_voice.schemas.triage import Category, Urgency

st.title("Review queue")

if "flash" in st.session_state:
    st.success(st.session_state.pop("flash"))

try:
    queue = api.get("/reviews")
except httpx.HTTPError as error:
    st.error(api.explain(error))
    st.stop()
if not queue:
    st.info("Nothing is waiting for review.")
    st.stop()

by_id = {r["id"]: r for r in queue}


def queue_label(report_id: str) -> str:
    r = by_id[report_id]
    return f"{r['urgency'].upper()} | {r['category']} | {r['status']} | {report_id}"


report_id = st.selectbox("Report", list(by_id), format_func=queue_label)
detail = api.get(f"/reports/{report_id}")

if detail["waiting_for"] == "review":
    p = detail["pending"]
    triage, routing, context = p["triage"], p["routing"], p["context"]
    st.subheader("Report")
    st.write(p["text"])
    if triage["language"] != "en":
        st.caption(f"Translation ({triage['language']}): {triage['english_text']}")
    st.write(f"**Summary:** {triage['summary']}")
    st.write(f"**Urgency:** {triage['urgency']}: {triage['urgency_reason']}")
    st.write(
        f"**Routing:** {routing['municipality']}, {routing['department']}: "
        f"{routing['reason']}"
    )
    if context:
        st.write(f"**Web check:** {context['finding']}: {context['summary']}")
        for source in context["sources"]:
            st.markdown(f"- [{source['title']}]({source['url']})")
    if p["duplicate"]["duplicate_of"]:
        st.write(f"**Possible duplicate of:** {p['duplicate']['duplicate_of']}")
    if detail["has_photo"]:
        st.image(api.get_bytes(f"/reports/{report_id}/photo"), width=400)

    categories, urgencies = [c.value for c in Category], [u.value for u in Urgency]
    with st.form("review"):
        action = st.radio("Decision", ["approve", "reject"], horizontal=True)
        category = st.selectbox(
            "Category", categories, index=categories.index(triage["category"])
        )
        urgency = st.selectbox(
            "Urgency", urgencies, index=urgencies.index(triage["urgency"])
        )
        department = st.text_input("Department", routing["department"])
        note = st.text_area("Note (optional)")
        sent = st.form_submit_button("Send decision", type="primary")
    if sent:
        decision = {"action": action, "note": note}
        if category != triage["category"]:
            decision["category"] = category
        if urgency != triage["urgency"]:
            decision["urgency"] = urgency
        if department != routing["department"]:
            decision["department"] = department
        live.watch(f"/reports/{report_id}/review", decision, "Decision sent")
        detail = api.get(f"/reports/{report_id}")

if detail["waiting_for"] == "draft":
    draft = detail["pending"]["draft"]
    st.subheader("Draft reply")
    with st.form("draft"):
        edited = st.text_area("Reply to the citizen", draft["body"], height=260)
        approve = st.form_submit_button("Approve", type="primary")
        reject = st.form_submit_button("Reject")
    if approve or reject:
        decision = {"action": "approve" if approve else "reject"}
        if approve and edited != draft["body"]:
            decision["text"] = edited
        try:
            result = api.send("POST", f"/reports/{report_id}/draft", json=decision)
        except httpx.HTTPError as error:
            st.error(api.explain(error))
        else:
            st.session_state.flash = f"{report_id}: {result['status']}"
            st.rerun()
