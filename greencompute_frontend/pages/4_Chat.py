import streamlit as st
import requests

# mainly composed from https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps#introduction

st.title("GreenCompute Recommender")


def chat_response(query: str):
    """Query the RAG model and return the response."""
    response = requests.post("http://localhost:8000/llm/rag", json={"query": query})
    return response.json()["body"]


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # User message
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = chat_response(prompt)

    # Assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})