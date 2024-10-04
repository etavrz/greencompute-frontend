import os
# Streamlit, a Python library used to create interactive web applications
import streamlit as st
# A Python library for making HTTP requests to interact with APIs.
import requests
#Imports the load_dotenv function from the dotenv module, which loads environment variables from a .env file into the program This allows you to use environment variables securely without hardcoding sensitive information like API routes..
from dotenv import load_dotenv


#Retrieves the value of the environment variable ROUTE. If ROUTE is not defined in the environment, it defaults to "localhost". This variable specifies the base URL (e.g., a server's address) for making requests to the API.
load_dotenv()
ROUTE = os.getenv("ROUTE", "localhost")

#Sets the title of the Streamlit application to "GreenCompute." This appears as a heading at the top of the web app.
st.title("GreenCompute")

# Get the data from the API
if st.button("Check the health of the API"):
    response = requests.get(f"http://{ROUTE}:8000/health")
    st.write(response.json())


#
