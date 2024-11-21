import json
import time

import requests
import streamlit as st

import greencompute_frontend.formatting as fmt

# Apply different formatting events
logo = "./greencompute_frontend/images/logo4.png"
fmt.add_logo(logo)
fmt.sidebar()
fmt.background()
fmt.title("GreenCompute Chat")


def stream_llm_response(query, chunk_size=10):
    url = "http://127.0.0.1:8000/api/llm/stream-rag"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    payload = {
        "body": query,
        "llm_id": "amazon.titan-text-premier-v1:0",
        "max_tokens": 512,
        "stop_sequences": [],
        "temperature": 0.7,
        "top_p": 0.8,
        "top_k": 10,
        "prompt": "cite",
    }

    with requests.post(url, headers=headers, data=json.dumps(payload), stream=True) as response:
        if response.status_code == 200:
            # Stream the response content
            for line in response.iter_lines(chunk_size=chunk_size):
                if line:  # Filter out keep-alive new lines
                    decoded_line = line.decode("utf-8")
                    for word in decoded_line.split(" "):
                        yield word + " "
                        time.sleep(0.08)
        else:
            yield f"Error: {response.status_code}, {response.text}"


def llm_response(query: str, context_size: int = 20):
    """Query the RAG model and return the response.

    Args:
        query (str): Query to send to the RAG model.
        context_size (int, optional): Context . Defaults to 20.

    Yields:
        str:
    """
    url = "http://127.0.0.1:8000/api/llm/rag"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    payload = {
        "body": query,
        "llm_id": "amazon.titan-text-premier-v1:0",
        "max_tokens": 512,
        "stop_sequences": [],
        "temperature": 0.7,
        "top_p": 0.8,
        "top_k": context_size,
        "prompt": "cite",
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_str: str = response.json()["response"]

    # Format the context items in markdown with the title and url
    references = ""
    titles = []
    for i, context_item in enumerate(response.json()["context"]):
        if context_item["doc_title"] in titles:
            continue
        titles.append(context_item["doc_title"])
        references += f"{i+1}. [{context_item['doc_title']}]({context_item['url']})\n"

    response_str += f"\n\n**References**:\n{references}"
    for word in response_str.split(" "):
        yield word + " "
        time.sleep(0.08)


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
if prompt := st.chat_input("What can we help with?"):
    # User message
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(llm_response(prompt))

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
