import base64
import json
import time

import requests
import streamlit as st

logo = "./images/logo4.png"


# mainly composed from https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps#introduction
def add_logo(logo, width):
    # Read the image and convert it to Base64
    with open(logo, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")

    # Inject CSS with Base64-encoded image into the sidebar
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: url("data:image/png;base64,{data}");
                background-repeat: no-repeat;
                padding-top: 150px;
                background-position: 10px 10px;
                background-size: {width};
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Call the add_logo function with the path to your local image
add_logo(logo, "200px")

st.markdown(
    """
    <style>
    /* Style for the sidebar content */
    [data-testid="stSidebarContent"] {
        background-color: white; /*#bac9b9; Sidebar background color */
    }
    /* Set color for all text inside the sidebar */
    [data-testid="stSidebar"] * {
        color: #3b8bc2 !important;  /* Text color */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Change the background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #d2e7ae;  /* #c0dc8f Light gray-green */
    }
    .custom-label{
        color: #3b8bc2;
        font-size: 18px;  /* Set the font size for text input, number input, and text area */
        padding: 10px;    /* Optional: adjust padding for better appearance */
    }
    p, li, span{
        color: #4b7170;
        font-size: 18px;  /* Set default font size */
        /* font-weight: bold;   Make the text bold */
    }

    </style>
    """,
    unsafe_allow_html=True,
)


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


st.title("GreenCompute Chat")


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
        response = st.write_stream(llm_response(prompt))

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
