import streamlit as st
import requests

st.title("GreenCompute")

# Get the data from the API
response = requests.get("http://localhost:8000/health")

if st.button("Check the health of the API"):
    st.write(response.json())
