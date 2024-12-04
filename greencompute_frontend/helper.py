import json
import time

import requests


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
        "top_n": 20,
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
        "max_tokens": 1024,
        "stop_sequences": [],
        "temperature": 0.3,
        "top_p": 0.7,
        "top_n": context_size,
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
