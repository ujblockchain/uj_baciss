"""Community Voice. Run: uv run streamlit run app/streamlit_app.py"""

import streamlit as st

st.set_page_config(page_title="Community Voice")

if "token" not in st.session_state:
    st.navigation([st.Page("pages/login.py", title="Sign in")]).run()
else:
    pages = [
        st.Page("pages/submit.py", title="Submit Report"),
        st.Page("pages/my_reports.py", title="My Reports"),
        st.Page("pages/review.py", title="Review Queue"),
        st.Page("pages/dashboard.py", title="Dashboard"),
    ]
    st.navigation(pages).run()
    if st.sidebar.button("Sign out"):
        del st.session_state["token"]
        st.rerun()
