"""Sign in."""

import httpx
import streamlit as st
from components import api

st.title("Sign in")
with st.form("login"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    sent = st.form_submit_button("Sign in", type="primary")
if sent:
    try:
        api.login(email, password)
    except httpx.HTTPError as error:
        st.error(api.explain(error))
    else:
        st.rerun()
