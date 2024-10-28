import json
import time

import streamlit as st
import requests

# mainly composed from https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps#introduction


def stream_llm_response(query, chunk_size=1):
    url = "http://127.0.0.1:8000/api/llm/stream-rag"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    payload = {
        "body": query,
        "llm_id": "amazon.titan-text-premier-v1:0",
        "max_tokens": 512,
        "stop_sequences": [],
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 10,
    }

    with requests.post(
        url, headers=headers, data=json.dumps(payload), stream=True
    ) as response:
        if response.status_code == 200:
            # Stream the response content
            for line in response.iter_lines(chunk_size=chunk_size):
                if line:  # Filter out keep-alive new lines
                    decoded_line = line.decode("utf-8")
                    words = decoded_line.split()
                    for word in words:
                        yield word + " "
                        time.sleep(0.08)
        else:
            yield f"Error: {response.status_code}, {response.text}"


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

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(stream_llm_response(prompt))

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
