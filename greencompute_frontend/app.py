import streamlit as st

pg_home = st.Page("pages/home.py", title="Home", icon=":material/info:")
pg_compute = st.Page("pages/compute.py", title="Compute", icon=":material/energy_savings_leaf:")
pg_chat = st.Page("pages/chat.py", title="Chat", icon=":material/chat:")
pg_about = st.Page("pages/about.py", title="About", icon=":material/group:")

pg = st.navigation([pg_home, pg_compute, pg_chat, pg_about])
st.set_page_config(page_title="GreenCompute", layout="wide", page_icon=":material/eco:")
pg.run()
