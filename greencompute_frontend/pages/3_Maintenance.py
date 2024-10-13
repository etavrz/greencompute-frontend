import os
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()
ROUTE = os.getenv("ROUTE", "localhost")

st.title("GreenCompute")

# Get the data from the API
if st.button("Check the health of the API"):
    response = requests.get(f"http://{ROUTE}:8000/health")
    st.write(response.json())
